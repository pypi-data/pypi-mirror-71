from django.conf import settings


class ConfigMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        version = settings.VERSION
        setattr(request, 'version', version)
        response = self.get_response(request)
        return response
