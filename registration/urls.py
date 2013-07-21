from django.conf.urls.defaults import *
from registration.views import RegistrationApi

urlpatterns = patterns('',
    url(r'^$', RegistrationApi(), (), 'registration_api'),
)