from rest_framework_jwt.authentication import JSONWebTokenAuthentication

class CsrfExemptTokenAuthentication(JSONWebTokenAuthentication):
    def enforce_csrf(self, request):
        return