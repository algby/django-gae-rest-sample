import base64

from django import http
from django.contrib.auth import authenticate
from rest.util import StatusCodes


def basicauth(realm = ""):
    """
    Decorator for views that checks the basic authentication header
    """
    def view_decorator(func):
        def wrapper(self,request, *args, **kwargs):
            if 'HTTP_AUTHORIZATION' in request.META:
                auth = request.META['HTTP_AUTHORIZATION'].split()
                if len(auth) == 2:
                    if auth[0].lower() == "basic":
                        username, password = base64.b64decode(auth[1]).split(':')
                        
                        user = authenticate(username=username, password=password)
                        
                        if user:
                            request.user = user
                            return func(self, request, *args, **kwargs)
                        
            response = http.HttpResponse()
            response.status_code = StatusCodes.FORBIDDEN
            response['WWW-Authenticate'] = 'Basic realm="%s"' % realm
            return response
        return wrapper
    return view_decorator


from django.core.cache import cache
import time

def throttle(max_requests, timeout=60*60, extra=''):
    """
    Decorator for views that throttles the requests from an user or ip address
    that exceeds the maximum number of requests in a given time
    """
    def view_decorator(func):
        def wrapper(self, request, *args, **kwargs):
            user = request.user;
            if user:
                ident = user.username
            else:
                ident = request.META.get('REMOTE_ADDR', None)
            
            if ident:
                ident += ':%s' % extra
        
                now = time.time()
                count, expiration = cache.get(ident, (1, None))
    
                if expiration is None:
                    expiration = now + timeout
    
                if count >= max_requests and expiration > now:
                    response = http.HttpResponse(status=StatusCodes.THROTTLED)
                    wait = int(expiration - now)
                    response.content = 'Throttled, wait %d seconds.' % wait
                    response['Retry-After'] = wait
                    return response
    
                cache.set(ident, (count+1, expiration), (expiration - now))
            
            return func(self, request, *args, **kwargs)
        return wrapper
    return view_decorator



