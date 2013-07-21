from django import http
from rest.util import StatusCodes

class RESTView(object):
    """
    Dispatches a request based on HTTP method
    """
    methods = ['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS']
    
    def __call__(self, request, *args, **kwargs):
        callback = getattr(self, request.method, None)
        if callback:
            return callback(request, *args, **kwargs)
        else:
            allowed_methods = self.get_allowed_methods()
            return http.HttpResponseNotAllowed(allowed_methods)
    
    def get_allowed_methods(self):
        return [m for m in self.methods if hasattr(self, m) and m != 'OPTIONS']

    def OPTIONS(self, request):
        allowed_methods = self.get_allowed_methods()
        response = http.HttpResponse(status=StatusCodes.OK)
        response['Allow'] = ', '.join(allowed_methods)
        return response