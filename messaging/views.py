from django import http

from rest.views import RESTView
from rest.util import JSONResponse, StatusCodes
from rest.decorators import basicauth, throttle

from messaging.models import Message
from django.utils.encoding import smart_str
from dateutil.parser import *
from django.contrib.auth.models import User

REALM = "MessagingApi"

class MessagingApi(RESTView):
    
    @basicauth(realm=REALM)
    @throttle(60,1*60,"GetMessages")
    def GET(self, request):
        """
        Returns the last 50 messages sent/received by the user of the request in JSON format
        
        The messages can be filtered specifying the parameters in the url:
            - to_user: the username of another user to get a specific conversation
            - datetime: the minimum datetime for the messages returned
        """
        sent = Message.objects.all().filter(from_user = request.user)
        received = Message.objects.all().filter(to_user = request.user)
        
        if request.GET.has_key('to_user'):
            
            to_user = None
            
            try:
                to_user = User.objects.get(username = request.GET['to_user'])
            except User.DoesNotExist:
                return http.HttpResponse(status=StatusCodes.NOT_FOUND)
            
            if to_user:
                sent = sent.filter(to_user = to_user)
                received = received.filter(from_user = to_user)
        
        if request.GET.has_key('datetime'):
            datetime = parse(smart_str(request.GET['datetime']))
            sent = sent.filter(datetime__gt =  datetime)
            received = received.filter(datetime__gt = datetime)
        
        sent = sent.order_by("-datetime")[:50]
        received = received.order_by("-datetime")[:50]
        
        messages = [item for item in sent]
        for item in received:
            messages.append(item)
        
        sorted_messages = sorted(messages, key=lambda m: m.datetime)
        
        return JSONResponse([item.format() for item in sorted_messages])
    
    @basicauth(realm=REALM)
    @throttle(10,1*60,"PostMessage")
    def POST(self, request):
        """
        Parses the JSON request to create a Message object
        """
        item = Message()
        item.parse(request)
        if not item:
            return http.HttpResponseBadRequest()
        
        item.save()
        
        return http.HttpResponse(status=StatusCodes.CREATED)
    
    @basicauth(realm=REALM)
    def DELETE(self, request):
        """
        Deletes all the messages on the database (must be a staff user)
        """
        if request.user.is_staff:
            Message.objects.all().delete()
            return http.HttpResponse(status=StatusCodes.DELETED)
        else:
            response = http.HttpResponseForbidden()
            return response
