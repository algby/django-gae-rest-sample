from django.db import models
from django.utils.encoding import force_unicode
from rest.util import JSONObject
import datetime
from django.contrib.auth.models import User

class Message(models.Model):
    """
    An object containing a message sent from an User to another
    """
    from_user = models.ForeignKey(User, related_name="from_user")
    to_user = models.ForeignKey(User, related_name="to_user")
    message = models.TextField()
    datetime = models.DateTimeField()
    
    def __unicode__(self):
        return self.message
    
    def format(self):
        """
        Returns a dictionary rapresenting the object in JSON format
        It can be used to create a JSONResponse
        """
        info = {
            'from_user': self.from_user.username,
            'to_user': self.to_user.username,
            'message': self.message,
            'datetime': force_unicode(self.datetime)
        }
        return info
        
    def parse(self, request):
        """
        Parses the content of an HttpRequest to a Message object
        """
        try:
            data = JSONObject(request)
            self.from_user = request.user
            self.to_user = User.objects.get(username=force_unicode(data.get('to_user','')))
            self.message = force_unicode(data.get('message', ''))
            self.datetime = datetime.datetime.now()
        except (ValueError, KeyError, TypeError):
            pass