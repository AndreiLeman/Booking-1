from django.conf.urls.defaults import *

from django.conf import settings
from django.conf.urls.static import static
import exambookings.views

urlpatterns = patterns('',
                       url(r'^$|^home/$',
                           'exambookings.views.home_page_view',
                           name='home'),
                       url(r'^team_bio/$',
                           'exambookings.views.team_bio_view',
                           name='team_bio'),
                       url(r'^signup/$',
                           'exambookings.views.sign_up_view',
                           name='sign_up'),
                       url(r'^signout/$',
                           'exambookings.views.sign_out_view',
                           name='signout'),
                       url(r'^booking/$',
                           'exambookings.views.booking_view',
                           name='booking'),
                       url(r'^static_page/(?P<file_name>.*\.html)$',
                           'exambookings.views.static_page'), # test out way to serve static page as though it were dynamic
                       url(r'^accounts/$',
                           'exambookings.views.user_profile_view'),
                       url(r'^booking/(?P<pk>\d+)/$',
                           'exambookings.views.update_booking_view',
#                           exambookings.views.UpdateBookingView.as_view(),
                           name='update_booking'),
) + static(settings.STATIC_URL, document_root='exambookings/static/')
