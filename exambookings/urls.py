from django.conf.urls.defaults import *

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
                       url(r'^home/$',
                           'exambookings.views.home_page',
                           name='home'),
                       url(r'^team_bio/$',
                           'exambookings.views.team_bio',
                           name='team_bio'),
                       url(r'^signout/$',
                           'userena.views.signout',
                           name='signout'),
                       url(r'^booking/$',
                           'exambookings.views.booking',
                           name='booking'),
                       url(r'^show_bookings/$',
                           'exambookings.views.show_bookings',
                           name='showBookings'),
                       url(r'^create_booking/$',
                           'exambookings.views.create_booking',
                           name='createBooking'),
                       url(r'^static_page/(?P<file_name>.*\.html)$',
                           'exambookings.views.static_page'), # test out way to serve static page as though it were dynamic
) + static(settings.STATIC_URL, document_root='exambookings/static/')
