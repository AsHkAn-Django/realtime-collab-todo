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
        queryset = SharedTask.objects.prefetch_related('participants')
        user = self.request.user

        for task in queryset:
            participants = list(task.participants.all())  
            task.show_participate_button = (user != task.creator and user not in participants)
            task.show_edit_button = (user == task.creator or user in participants)
            task.show_delete_button = (user == task.creator)

        return queryset
    
    

class SharedSubTaskUpdateView(generic.UpdateView):
    model = SubTask
    form_class = SubTaskForm
    template_name = "shared_task/shared_subtask_update.html"
    success_url = reverse_lazy('shared_task:shared_task_list')



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