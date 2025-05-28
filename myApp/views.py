from django.urls import reverse_lazy
from django.views import generic, View
from django.shortcuts import render,get_object_or_404
from django.utils import timezone
from django.http import JsonResponse

from .models import Task, Category
from .forms import TaskForm, CategoryForm, FilterForm



class IndexView(generic.TemplateView):
    template_name = "myApp/index.html"
    
 
      
def filter_list(request):
    tasks = Task.objects.all()
    form = FilterForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            category = form.cleaned_data['category']
            priority = form.cleaned_data['priority']
            if category:
                tasks = tasks.filter(category_id=category)
            if priority:
                tasks = tasks.filter(priority=priority)
    else:
        form = FilterForm()

    print(tasks)
    return render(request, 'myApp/filter_list.html', {'tasks': tasks, 'form': form})



class AllTasksView(generic.ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = "myApp/all_tasks.html"
    
    # TODO: use the model method instead 
    def get_queryset(self):
        # get the time of now
        now = timezone.now()
        # Use date__lte(less than or equal) to filter everything before now
        # and the items which the overdue is false
        # then update those items to True overdue
        Task.objects.filter(deadline__lte=now, overdue=False).update(overdue=True)
        # and updates the ones which were edited to a new overdue
        Task.objects.filter(deadline__gte=now, overdue=True).update(overdue=False)
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['form'] = FilterForm
        return context

    

class AddCategoryView(generic.CreateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('myApp:all_tasks')
    template_name = "myApp/add_category.html"
    
    def form_valid(self, form):
        """Duplicate Checker."""
        # we didn't use form.cleaned_data['title'] because it raise an error if there is no value
        category_name = form.cleaned_data.get('title')
        if Category.objects.filter(title__iexact=category_name).exists():
            form.add_error('title', 'This category already exists.')
            return self.form_invalid(form)
        return super().form_valid(form)



class AddTaskView(generic.CreateView):
    model = Task
    form_class = TaskForm
    template_name = "myApp/add_task.html"

    def get_success_url(self):
        return reverse_lazy('myApp:category_filter_list', args=[self.object.category.id])
    
    
class EditTaskView(generic.UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'myApp/edit_task.html'
    success_url = reverse_lazy('myApp:all_tasks')


class DeleteTaskView(generic.DeleteView):
    model = Task
    template_name = 'myApp/delete_task.html'
    success_url = reverse_lazy('myApp:all_tasks')
    

class TaskListJson(View):
    """Returns all tasks in JSON format suitable for FullCalendar."""
    def get(self, request, *args, **kwargs):
        tasks = Task.objects.all()

        events = []
        for t in tasks:
            events.append({
                'id': t.id,
                'title': t.title,
                'start': t.deadline.isoformat(),
                'allDay': False,
                'url': f'/tasks/{t.id}/',
            })

        return JsonResponse(events, safe=False)

    
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'myApp/task_detail.html', {'task': task})

