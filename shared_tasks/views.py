from django.shortcuts import render
from django.views import generic
from .models import TaskRecord, SubTask, SharedTask
from .forms import TaskRecordForm, SubTaskForm, ShareTaskForm
from django.contrib.auth.mixins import LoginRequiredMixin



class SharedTaskListView(LoginRequiredMixin, generic.ListView):
    model = SharedTask
    context_object_name = 'shared_tasks'
    template_name = "shared_tasks/shared_tasks_list.html"

