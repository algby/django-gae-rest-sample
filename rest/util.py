from django import http
from django.conf import settings
from django.utils import simplejson

class JSONResponse(http.HttpResponse):
    """
    Creates an instance of HttpResponse containing JSON content
    """
    def __init__(self, data):
        indent = 2 if settings.DEBUG else None
        mime = ("text/javascript" if settings.DEBUG 
                                  else "application/json")
        super(JSONResponse, self).__init__(
            content = simplejson.dumps(data, indent=indent),
            mimetype = mime,
        )
        
def JSONObject(request):
    """
    Returns a JSON object based on the content of an HttpRequest
    """
    return simplejson.loads(request.raw_post_data)

class StatusCodes(object):
    """
    Provides a verbose list of Status Codes for HttpResponse objects
    """ 
    OK = 200
    CREATED = 201
    DELETED = 204
    BAD_REQUEST = 400
    FORBIDDEN = 401
    NOT_FOUND = 404
    DUPLICATE_ENTRY = 409
    NOT_HERE = 410
    INTERNAL_ERROR = 500
    NOT_IMPLEMENTED = 501
    THROTTLED = 503