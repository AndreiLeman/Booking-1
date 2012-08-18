from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext

from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView

from exambookings.models import Booking
from exambookings.forms import CreateBookingForm

from exambookings.viewsHelpers import reverse_lazy, StaffOnlyViewMixin

class CreateBooking(StaffOnlyViewMixin, CreateView):
#    model = Booking
#    template_name_suffix = "_create_form" # looks for template "booking_create_form.html"
#    context_object_name = "create_booking"
    template_name = 'exambookings/make_a_booking.html'
    form_class = CreateBookingForm
    success_url = reverse_lazy('showBookings')

    # def render_to_response(self, context, **response_kwargs):
    #     #return django.shortcuts.render_to_response('exambookings/make_a_booking.html', {})
    #     context['forma'] = CreateBookingForm()
    #     return super(CreateBooking, self).render_to_response(context, **response_kwargs)
        

class ShowBookings(StaffOnlyViewMixin, ListView):
    model = Booking
    context_object_name="bookings_list"
    template_name = 'exambookings/bookings_list.html'

    def get_queryset(self):
        if (self.request.user.has_perm('exambookings.exam_center_view')):
            bookings = Booking.objects.all()
        elif (self.request.user.has_perm('exambookings.teacher_view')):
            #theStaffBaseProfile = get_object_or_404(BaseProfile, emailAddress__exact=self.request.user.email)
            bookings = Booking.objects.filter(courseTeacher=self.request.user)
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
        
from userena.views import signin
def home_page(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('showBookings'))
    return signin(request,
                  template_name='exambookings/home.html',
                  extra_context={'redirect_to':reverse('showBookings'),})
@login_required
def static_page(request, file_name):
    return render_to_response('exambookings/static_pages/'+file_name, {})


