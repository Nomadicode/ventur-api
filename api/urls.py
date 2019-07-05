"""driftr_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.urls import path, re_path, include
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
from django.contrib import admin

from rest_framework_jwt.views import refresh_jwt_token, verify_jwt_token
from rest_auth.views import (
    LoginView, LogoutView, UserDetailsView, PasswordChangeView,
    PasswordResetView, PasswordResetConfirmView
)

from users.social_views import FacebookLogin
from graphene_django.views import GraphQLView

urlpatterns = [
    re_path('^', include('django.contrib.auth.urls')),
    re_path('^admin/?', admin.site.urls),
    re_path('^auth/register/?', include(('rest_auth.registration.urls', 'users'), namespace='users'), name="register"),
    re_path('^auth/', include('rest_auth.urls')),
    re_path('^accounts/', include('allauth.urls')),

    re_path('^auth/facebook', FacebookLogin.as_view(), name="fb_login"),
    
    re_path('^auth/refresh-token', refresh_jwt_token),
    re_path('^auth/verify-token', verify_jwt_token),

    re_path('^friendship/', include('friendship.urls')),

    re_path('^graphql', csrf_exempt(GraphQLView.as_view(graphiql=True)), name="graphql"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
