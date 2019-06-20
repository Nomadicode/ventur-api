from rest_framework.authentication import JSONWebTokenAuthentication

class CsrfExemptTokenAuthentication(JSONWebTokenAuthentication):
    def enforce_csrf(self, request):
        return