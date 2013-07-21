from django import http

from rest.views import RESTView
from rest.util import JSONObject, StatusCodes
from django.utils.encoding import force_unicode
from rest.decorators import throttle

from django.contrib.auth.models import User

class RegistrationApi(RESTView):
    
    @throttle(1,1*60,"UserRegistration")
    def POST(self, request):
        """
        Accepts a JSON request containing:
            - username
            - email
            - password
        and saves the User on the backend
        """
        try:
            data = JSONObject(request)
        except:
            return http.HttpResponseBadRequest()
        
        username = force_unicode(data.get('username',''))
        email = force_unicode(data.get('email',''))
        password = force_unicode(data.get('password',''))
        
        if username == '' or email == '' or password == '':
            return http.HttpResponseBadRequest()
        
        try:
            User.objects.get(username=username)
            return http.HttpResponse(status=StatusCodes.DUPLICATE_ENTRY)
        except User.DoesNotExist:
            User.objects.create_user(username,email,password)
            return http.HttpResponse(status=StatusCodes.CREATED)
        
