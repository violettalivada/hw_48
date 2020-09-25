from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from accounts.views import *

app_name = 'accounts'

urlpatterns = []