from django.conf.urls.defaults import *
from django.contrib import admin

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    (r'^$', 'project.views.index',(),'site_index'),
    (r'^admin/', include(admin.site.urls)),
    (r'^api/registration/', include('registration.urls')),
    (r'^api/messaging/', include('messaging.urls')),
    (r'^i18n/', include('django.conf.urls.i18n')),
)
