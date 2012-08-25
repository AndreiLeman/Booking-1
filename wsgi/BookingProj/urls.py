from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
#                       url(r'^poll/', include('pollApp.urls')),
                       url(r'^exambookings/', include('exambookings.urls')),
    # Examples:
    # url(r'^$', 'exampleApp.views.home', name='home'),
    # url(r'^exampleApp/', include('exampleApp.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
                           url(r'^admin/', include(admin.site.urls)),
                           url(r'^accounts/', include('userena.urls')),
                           url(r'^$', redirect_to, {'url': '/exambookings/home'}),

)
