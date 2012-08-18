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

def bookings_list_for(user):
    """ returns dictionary of bookings the user can view """
    if (user.has_perm('exambookings.exam_center_view')):
        bookings = Booking.objects.all()
    elif (user.has_perm('exambookings.teacher_view')):
        bookings = Booking.objects.filter(courseTeacher=user)
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

    return bookings_list


@staff_only_view
def booking(request):
    """ shows bookings available to be seen by logged-in user
    also provides a form to create a new booking appointment
    """
    ctx = {}
    ctx.update(csrf(request))
    ctx['bookings_list'] = bookings_list_for(request.user)
    
    form = CreateBookingForm()
    if request.method == 'POST':
        form = CreateBookingForm(request.POST, request.FILES)
        form.instance.courseTeacher = request.user
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('booking'))
    
    ctx['form'] = form
    return render_to_response('exambookings/booking.html', ctx)


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

