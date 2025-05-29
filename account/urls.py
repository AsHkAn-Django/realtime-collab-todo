from django.urls import path, include
from . import views


app_name = 'account'


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('signup/', views.UserCreateView.as_view(), name='signup'),
]