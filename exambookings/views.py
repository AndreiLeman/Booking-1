from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext

from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView

from exambookings.models import Booking
from exambookings.forms import CreateBookingForm

from django.core.urlresolvers import reverse
from exambookings.viewsHelpers import reverse_lazy, StaffOnlyViewMixin, staff_only_view


class CreateBooking(StaffOnlyViewMixin, CreateView):
#    model = Booking
#    template_name_suffix = "_create_form" # looks for template "booking_create_form.html"
#    context_object_name = "create_booking"
    template_name = 'exambookings/make_a_booking.html'
    form_class = CreateBookingForm
    success_url = reverse_lazy('showBookings')

    def get_initial(self):
        """ this will set the initial value in the form, but
        if form excludes this field, then when form is processed
        courseTeacher field would not be set and can't be saved
        into the database.  See form_valid instead.
        """
        return {'courseTeacher': self.request.user,}

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.        
        form.instance.courseTeacher = self.request.user
        return super(CreateBooking, self).form_valid(form)


    # def render_to_response(self, context, **response_kwargs):
    #     #return django.shortcuts.render_to_response('exambookings/make_a_booking.html', {})
    #     context['forma'] = CreateBookingForm()
    #     return super(CreateBooking, self).render_to_response(context, **response_kwargs)

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

from userena.views import signin
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

