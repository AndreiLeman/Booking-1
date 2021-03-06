#from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
#from django.template import RequestContext

from django.contrib.auth.models import User
from exambookings.models import Booking, Period
from exambookings.forms import CreateBookingForm, ExamBookingSignupForm, ExamBookingAuthForm, UpdateBookingForm

import userena.views
import userena.settings

from django.core.urlresolvers import reverse
from exambookings.viewsHelpers import *

import datetime

@staff_only_view
def context_for_create_or_check_booking(request):
    """ shows bookings available to be seen by logged-in user
    also provides a form to create a new booking appointment.
    return 0 if caller should redirect to another page without context
    """
    ctx = create_standard_csrf_context(request)
    ctx['bookings_list'] = Booking.getAllObjectsDataNormalizedForUser(request.user) #bookings_list_for(request.user, orderedFields = True)

    now = datetime.datetime.now()
    DAYS_OF_STATS_TO_SHOW = 5
    ctx['availableAppts'] = Booking.apptStats(DAYS_OF_STATS_TO_SHOW, showApptsAvailable = True)
    ctx['refreshTime'] =  now.strftime("%b %d, %I:%M %p")

    if request.user.has_perm('exambookings.exam_center_view'):
        ctx['exam_center_view'] = True    
    
    form = CreateBookingForm(initial={'testDate':datetime.datetime.now()})
    if request.method == 'POST':
        form = CreateBookingForm(request.POST, request.FILES)

        if form.is_valid():
            perId = form.cleaned_data['testBeginTime']
            form.instance.courseTeacher = request.user
            form.instance.testBeginTime = Period.startTimeOfPeriodIdOnDay(perId, form.cleaned_data['testDate'])
            form.instance.testEndTime = milTimeAfterMinutes(form.instance.testBeginTime, form.cleaned_data['testDuration'])
        # double is_valid() call is required. testBeginTime model
        # field is hacked to support storing period IDs prior to
        # save() but should always be set to period start times when
        # save()ing
        if form.is_valid():
            form.save()
            return 0
    
    ctx['form'] = form
    ctx['form_fields_groups'] = form_fields_groups_for_view(request.user, form)
    return ctx
    
@staff_only_view
def create_booking_view(request):
    """ shows bookings available to be seen by logged-in user
    also provides a form to create a new booking appointment
    """
    ctx = context_for_create_or_check_booking(request)
    if (ctx == 0):
        return HttpResponseRedirect(reverse('create_booking'))
    return render_to_response('exambookings/booking.html', ctx)
    
@staff_only_view
@authorized_user_of_this_booking_only_view
def update_booking_view(request, pk):
    return dup_or_update_booking(request, pk, False)

@staff_only_view
@authorized_user_of_this_booking_only_view
def update_booking_success_view(request, pk):
    return dup_or_update_booking(request, pk, False, True)

@staff_only_view
@authorized_user_of_this_booking_only_view
def dup_and_update_booking_view(request, pk):
    return dup_or_update_booking(request, pk, True)

def dup_or_update_booking(request, pk, duplicate=False, saved=False):
    ctx = create_standard_csrf_context(request)
    ctx['bookings_list'] = Booking.getAllObjectsDataNormalizedForUser(request.user) #bookings_list_for(request.user, orderedFields = True)
    
    if request.user.has_perm('exambookings.exam_center_view'):
        exam_center_view = True
        ctx['exam_center_view'] = True
    else:
        exam_center_view = False

    appt = get_object_or_404(Booking, id__iexact=pk)
    if duplicate:
        appt.pk = None
    
    if request.method == 'POST':
        if not exam_center_view:
            post = request.POST.copy()
            post.setlist('courseTeacher', [request.user.pk])
            form = UpdateBookingForm(post, instance=appt)
        else:
            form = UpdateBookingForm(request.POST, instance=appt)

        if form.is_valid():
            perId = form.cleaned_data['testBeginTime']
            formTestDate = form.cleaned_data['testDate']
            periodStartTime = Period.startTimeOfPeriodIdOnDay(perId, formTestDate)
            form.instance.testBeginTime = periodStartTime
            form.instance.testEndTime = milTimeAfterMinutes(periodStartTime, form.cleaned_data['testDuration'])
        # double is_valid() call is required. testBeginTime model
        # field is hacked to support storing period IDs prior to
        # save() but should always be set to period start times when
        # save()ing            
        if form.is_valid():
            form.save()
            pk = form.instance.pk
            return HttpResponseRedirect(reverse('update_booking_success', kwargs={'pk':pk}))
    else:
        form = UpdateBookingForm(instance=appt, initial={'testBeginTime':Period.idOfPeriodStartTimeOnDay(appt.testBeginTime, appt.testDate)})
    
    ctx['form'] = form
    ctx['form_fields_groups'] = form_fields_groups_for_view(request.user, form)
    ctx['saved'] = saved
    if duplicate:
        useTemplate = 'exambookings/duplicate_booking.html'
    else:
        useTemplate = 'exambookings/update_booking.html'
    return render_to_response(useTemplate, ctx)

@staff_only_view
@authorized_user_of_this_booking_only_view
def set_booking_completed_view(request, pk):
    if request.method == 'POST':
        appt = get_object_or_404(Booking, id__iexact=pk)
        appt.testCompleted = True
        try:
            appt.save()
        except ValidationError as e:
            pass # errors contained in e.message_dict
    return HttpResponseRedirect(reverse('create_booking'))

@staff_only_view
@authorized_user_of_this_booking_only_view
def set_no_show_view(request, pk):
    if request.method == 'POST':
        appt = get_object_or_404(Booking, id__iexact=pk)
        appt.noShow = True
        try:
            appt.save()
        except ValidationError as e:
            pass # errors contained in e.message_dict
    return HttpResponseRedirect(reverse('create_booking'))


@staff_only_view
@authorized_user_of_this_booking_only_view
def delete_booking_view(request, pk):
    """ GET will prompt to delete.
    POST will delete!
    """
    ctx = create_standard_csrf_context(request)
    if request.user.has_perm('exambookings.exam_center_view'):
        ctx['exam_center_view'] = True

    appt = get_object_or_404(Booking, id__iexact=pk)

    if request.method == 'POST':
        appt.delete()
        return HttpResponseRedirect(reverse('create_booking'))

    ctx['bookingData'] = appt.getNormalizedDataOfFields(orderedFields=True, incl_false_bool_fields=True)
    return render_to_response('exambookings/delete_booking_confirm.html', ctx)



def sign_up_view(request):
    ctx = create_standard_context(request)
    return userena.views.signup(request,
                                signup_form=ExamBookingSignupForm,
                                success_url=reverse('sign_up_success'),
                                template_name='exambookings/sign_up.html',
                                extra_context=ctx)


def sign_up_success_view(request):
    ctx = create_standard_context(request)
    ctx.update({'userena_activation_required': userena.settings.USERENA_ACTIVATION_REQUIRED,
                'userena_activation_days': userena.settings.USERENA_ACTIVATION_DAYS})
    return render_to_response('exambookings/signup_complete.html', ctx)


def sign_out_view(request):
#    ctx = create_standard_context(request)
    return userena.views.signout(request)
                                # template_name='exambookings/sign_up.html',

 

def home_page_view(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('create_booking'))

    ctx = create_standard_context(request)
    ctx['redirect_to'] = reverse('create_booking')
    return userena.views.signin(request,
                                template_name='exambookings/home.html',
                                extra_context=ctx,
                                auth_form=ExamBookingAuthForm)
@staff_only_view
def check_booking(request):
    """ shows bookings available to be seen by logged-in user
    also provides a form to create a new booking appointment
    """
    ctx = context_for_create_or_check_booking(request)
    if (ctx == 0):
        return HttpResponseRedirect(reverse('create_booking'))
    return render_to_response('exambookings/check_booking.html', ctx)



def team_bio_view(request):
    ctx = create_standard_context(request)
    return render_to_response('exambookings/static_pages/team_bio.html', ctx)


@login_required
def static_page(request, file_name):
    return render_to_response('exambookings/static_pages/'+file_name, {})

@login_required
def user_profile_view(request):
    """ users in exambookings app have usernames assigned randomly so
    they don't know their own username (only their email address)
    so to access their user accounts they have to sign in first, then
    this view will redirect to the correct userena user account profile
    """
    user = get_object_or_404(User, email__iexact=request.user.email)
    return HttpResponseRedirect(reverse('userena_profile_detail', kwargs={'username': user.username}))
