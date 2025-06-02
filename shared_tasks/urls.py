from . import views
from django.urls import path


app_name = 'shared_tasks'

urlpatterns = [
    path('', views.SharedTaskListView.as_view(), name='shared_task_list'),
    path('participation_request/<int:pk>/', views.ParticipationRequestCreateView.as_view(), name='participation_request'),
    path('request_project_list/', views.RequestProjectListView.as_view(), name='request_project_list'),
    path('request_project_list/accept/<int:pk>/', views.accept_user, name='accept_user'),
    path('request_project_list/refuse/<int:pk>/', views.refuse_user, name='refuse_user'),

]