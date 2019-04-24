"""emotions-and-me-backend URL Configuration

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
from django.contrib import admin
from django.urls import path, re_path, include
import Hello.views as hello_views
import webcam.views as webcam_views
import livestream.views as livestream_views
import audio_emotions.views as audio_views
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

urlpatterns = [
    path(r'check_video', livestream_views.CheckVideoView.as_view()),
    path('admin/', admin.site.urls),
    # path(r'', hello_views.AllTech.as_view()),
    path('health/', include('health_check.urls')),
    # re_path(r'(?P<pk>\d+)', hello_views.TechView.as_view()),
    path(r'analyze_emotion', webcam_views.ImageView.as_view()),
    path(r'get_video', livestream_views.UrlView.as_view()),
    path('core/', include('core.urls')),
    path('token-auth/', obtain_jwt_token),
    path('token-refresh/', refresh_jwt_token),
    path('token-verify/', verify_jwt_token),
    path('assignments/', include('assignments.urls')),
    path(r'audio_emotions', audio_views.AudioView.as_view()),
]
