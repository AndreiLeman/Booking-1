from django.conf.urls.defaults import *

from django.conf import settings
from django.conf.urls.static import static

from django.views.generic import DetailView, ListView
#from exambookings.models import Poll
from exambookings.views import ShowBookings, CreateBooking


urlpatterns = patterns('',
    url(r'^show_bookings/$',
        ShowBookings.as_view(),
        name='showBookings'),
    url(r'^create_booking/$', CreateBooking.as_view()),                       
    url(r'^static_page/(?P<file_name>.*\.html)$', 'exambookings.views.static_page'), # test out way to serve static page as though it were dynamic
) + static(settings.STATIC_URL, document_root='exambookings/static/')
