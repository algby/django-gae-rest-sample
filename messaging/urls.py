from django.conf.urls.defaults import *
from messaging.views import MessagingApi

urlpatterns = patterns('',
    url(r'^$', MessagingApi(), (), 'messaging_api'),
)