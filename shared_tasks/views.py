from django.views import generic
from .models import TaskRecord, SubTask, SharedTask, ParticipationRequest
from .forms import TaskRecordForm, SubTaskForm, ShareTaskForm, ParticipationRequestForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy



class SharedTaskListView(LoginRequiredMixin, generic.ListView):
    context_object_name = 'shared_tasks'
    template_name = "shared_task/shared_task_list.html"

    def get_queryset(self):
        queryset = SharedTask.objects.all()
        for task in queryset:
            task.show_participate_button = ( self.request.user != task.creator and self.request.user not in task.participants.all())
        return queryset
    

class ParticipationRequestCreateView(generic.CreateView):
    model = ParticipationRequest
    form_class = ParticipationRequestForm
    template_name = "shared_task/participation_request.html"
    success_url = reverse_lazy('shared_task:shared_task_list')

    def form_valid(self, form):
        task_id = self.kwargs.get('pk')
        task = get_object_or_404(SharedTask, pk=task_id)
        if ParticipationRequest.objects.filter(user=self.request.user, task=task).exists():
            messages(self.request, 'You have already sent a request for this project. Please just wait for the response.')
            return self.form_invalid(form)
        form.instance.user = self.request.user
        form.instance.task = task
        messages.success(self.request, 'Your request has been sent successfully. The project owner will inform you ASAP.')
        return super().form_valid(form)
    

class RequestProjectListView(generic.ListView):
    model = ParticipationRequest
    template_name = "shared_task/request_project_list.html"
    context_object_name = "requests"


def accept_user(request, pk):
    request = get_object_or_404(ParticipationRequest, pk=pk)
    request.accept()
    return redirect('shared_task:request_project_list')

def refuse_user(request, pk):
    request = get_object_or_404(ParticipationRequest, pk=pk)
    request.refuse()
    return redirect('shared_task:request_project_list')