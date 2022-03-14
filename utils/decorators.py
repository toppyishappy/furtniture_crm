from django.http import HttpResponse
import json

from user.models import User


def json_response(func):
    """
    A decorator thats takes a view response and turns it
    into json. If a callback is added through GET or POST
    the response is JSONP.
    """
    def decorator(request, *args, **kwargs):
        objects = func(request, *args, **kwargs)
        if isinstance(objects, HttpResponse):
            return objects
        try:
            data = json.dumps(objects)
            if 'callback' in request.GET:
                # a jsonp response!
                data = '%s(%s);' % (request.GET['callback'], data)
                return HttpResponse(data, "text/javascript")
            if 'callback' in request.POST:
                # a jsonp response!
                data = '%s(%s);' % (request.POST['callback'], data)
                return HttpResponse(data, "text/javascript")
        except:
            data = json.dumps(str(objects))
        return HttpResponse(data, "application/json")
    return 
    

def is_sale(func):
    def decorator(request, *args, **kwargs):
        if request.user.role == User.SALE:
            return
    return

