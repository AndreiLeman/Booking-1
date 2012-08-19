from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.context_processors import csrf

from django.contrib.auth.models import User
from exambookings.models import Booking
from exambookings.forms import CreateBookingForm, ExamBookingSignupForm, ExamBookingAuthForm, UpdateBookingForm

import userena.views

from django.core.urlresolvers import reverse
from exambookings.viewsHelpers import reverse_lazy, staff_only_view

def create_standard_context(request):
    ctx = {}
    if request.user.is_authenticated():
        ctx['user_logged_in'] = True
    return ctx

def create_standard_csrf_context(request):
    ctx = create_standard_context(request)
    ctx.update(csrf(request))
    return ctx


BOOKING_fieldNames_ordered = ["studentFirstName",
                              "studentLastName",
                              'studentGrade',
                              "testCourseName",
                              "courseTeacher",
                              'testName',
                              'testDuration',
                              'testDate',
                              "testPeriod",
                              "examCenter",
                              'extendedTimeAccomodation',
                              'computerAccomodation',
                              'scribeAccomodation',
                              'enlargementsAccomodation',
                              'readerAccomodation',
                              'isolationQuietAccomodation',
                              'ellDictionaryAllowance',
                              'calculatorManipulativesAllowance',
                              'openBookNotesAllowance',
                              'computerInternetAllowance',
                              'englishDictionaryThesaurusAllowance',
                              'otherAllowances']

def bookings_list_for(user, incl_false_bool_fields = False):
    """ returns dictionary of bookings the user can view """
    if (user.has_perm('exambookings.exam_center_view')):
        bookings = Booking.objects.all()
    elif (user.has_perm('exambookings.teacher_view')):
        bookings = Booking.objects.filter(courseTeacher=user)
    else:
        bookings = []

    bookings_list = []
    for booking in bookings:
        bookingData = {'editUrl':{'value':reverse('update_booking',
                                                  kwargs={'pk':booking.pk}),
                                  'verbose_name': "Edit Link",
                                  'help_text': '',
                                  'name': 'editUrl'}}
        for fieldname in BOOKING_fieldNames_ordered:
            fieldData = booking.fieldDataOf(fieldname)
            if incl_false_bool_fields or fieldData['value'] != False:
                bookingData.update({fieldname: fieldData})
                    
            # note bookingData is an unordered dictionary!
        bookings_list.append(bookingData)
    return bookings_list


def bookings_list_fields_ordered_for(user, incl_false_bool_fields = False):
    bookings_list = bookings_list_for(user, incl_false_bool_fields)
    for i in range(len(bookings_list)):
        bookingData = bookings_list[i]
        bookingDataOrderedList = [bookingData['editUrl']]
        for f in BOOKING_fieldNames_ordered:
            if f in bookingData:
                bookingDataOrderedList.append(bookingData[f])
        bookings_list[i] = bookingDataOrderedList
    return bookings_list
    

@staff_only_view
def create_booking_view(request):
    """ shows bookings available to be seen by logged-in user
    also provides a form to create a new booking appointment
    """
    ctx = create_standard_csrf_context(request)
    ctx['bookings_list'] = bookings_list_fields_ordered_for(request.user)
    
    form = CreateBookingForm()
    if request.method == 'POST':
        form = CreateBookingForm(request.POST, request.FILES)
        form.instance.courseTeacher = request.user
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('create_booking'))
    
    ctx['form'] = form
    return render_to_response('exambookings/booking.html', ctx)


@staff_only_view
def update_booking_view(request, pk):
    ctx = create_standard_csrf_context(request)
    ctx['bookings_list'] = bookings_list_fields_ordered_for(request.user)
    
    if request.user.has_perm('exambookings.exam_center_view'):
        exam_center_view = True
        ctx['exam_center_view'] = True
    else:
        exam_center_view = False

    appt = get_object_or_404(Booking, id__iexact=pk)
    if request.method == 'POST':
        if not exam_center_view:
            post = request.POST.copy()
            post.setlist('courseTeacher', [request.user.pk])
            form = UpdateBookingForm(post, instance=appt)
        else:
            form = UpdateBookingForm(request.POST, instance=appt)
        
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('update_booking', kwargs={'pk':pk}))
    else:
        form = UpdateBookingForm(instance=appt)
    
    ctx['form'] = form
    return render_to_response('exambookings/update_booking.html', ctx)


def sign_up_view(request):
    ctx = create_standard_context(request)
    return userena.views.signup(request,
                                signup_form=ExamBookingSignupForm,
                                success_url=reverse('home'),
                                template_name='exambookings/sign_up.html',
                                extra_context=ctx)


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
