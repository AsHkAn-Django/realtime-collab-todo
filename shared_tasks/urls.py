from . import views
from django.urls import path


app_name = 'shared_tasks'

urlpatterns = [
    path('', views.SharedTaskListView.as_view(), name='shared_tasks_list'),
]