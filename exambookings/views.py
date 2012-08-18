from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.context_processors import csrf

from exambookings.models import Booking
from exambookings.forms import CreateBookingForm
from userena.views import signin

from django.core.urlresolvers import reverse
from exambookings.viewsHelpers import reverse_lazy, staff_only_view


@staff_only_view
def create_booking(request):
    ctx = {}
    ctx.update(csrf(request))
    
    form = CreateBookingForm()
    if request.method == 'POST':
        form = CreateBookingForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.courseTeacher = request.user
            form.save()
            return HttpResponseRedirect(reverse('showBookings'))
    
    ctx['form'] = form
    return render_to_response('exambookings/make_a_booking.html', ctx)


@staff_only_view
def show_bookings(request):
    if (request.user.has_perm('exambookings.exam_center_view')):
        bookings = Booking.objects.all()
    elif (request.user.has_perm('exambookings.teacher_view')):
        bookings = Booking.objects.filter(courseTeacher=request.user)
    else:
        bookings = []
        
    bookings_list = []
    for booking in bookings:
        bookings_list.append(
            {"studentFirstName": booking.studentFirstName,
             "studentLastName": booking.studentLastName,
             "course": booking.testCourseName,
             "test": booking.testName,
             "examCenter": booking.examCenter,
             "courseTeacher": '' + booking.courseTeacher.first_name + ' ' + booking.courseTeacher.last_name,
             "workPeriod": booking.testPeriod })

    return render_to_response('exambookings/bookings_list.html',
                              {'bookings_list': bookings_list,})


def home_page(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('showBookings'))
    return signin(request,
                  template_name='exambookings/home.html',
                  extra_context={'redirect_to':reverse('showBookings'),})


def team_bio(request):
    return render_to_response('exambookings/static_pages/team_bio.html', {})


@login_required
def static_page(request, file_name):
    return render_to_response('exambookings/static_pages/'+file_name, {})

