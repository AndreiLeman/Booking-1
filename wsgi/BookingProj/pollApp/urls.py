from django.conf import settings
from django.conf.urls.defaults import *

from django.views.generic import DetailView, ListView, TemplateView

from pollApp.views import *
from pollApp.models import *

urlpatterns = patterns('',
                       url(r'^$',
                           ListView.as_view(
            queryset=Poll.objects.order_by('-pub_date')[:5],
            context_object_name='latest_poll_list',
            template_name='pollApp/index.html'),
                           name='pollAppHome'),

                       url(r'^(?P<pk>\d+)/$',
                           DetailView.as_view(
            model=Poll,
            template_name='pollApp/detail.html'),
                           name='pollDetail'),

                       url(r'^(?P<pk>\d+)/results/$',
                           DetailView.as_view(
            model=Poll,
            template_name='pollApp/results.html'),
                           name='poll_results'),

                       url(r'^(?P<poll_id>\d+)/vote/$', 'pollApp.views.vote'),

                       )
