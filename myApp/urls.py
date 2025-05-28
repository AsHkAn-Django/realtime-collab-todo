from django.urls import path
from . import views

app_name = 'myApp'
urlpatterns = [
  
	path('filter/', views.filter_list, name='filter_list'),
    path('delete_task/<int:pk>', views.DeleteTaskView.as_view(), name='delete_task'),
	path('category_list/tasks/', views.AllTasksView.as_view(), name='all_tasks'),
	path('add_category/', views.AddCategoryView.as_view(), name='add_category'),
    path('edit_task/<int:pk>', views.EditTaskView.as_view(), name='edit_task'),
	path('add_task/', views.AddTaskView.as_view(), name='add_task'),
    path('tasks/<int:pk>/', views.task_detail, name='task-detail'),
    path('api/tasks/', views.TaskListJson.as_view(), name='task-list-json'),
	path('', views.IndexView.as_view(), name='home'),
]
