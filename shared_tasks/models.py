from django.db import models
from django.conf import settings

        

class SharedTask(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL)
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
	    return self.title



class SubTask(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    shared_task = models.ForeignKey(SharedTask, related_name='shared_sub_tasks', on_delete=models.CASCADE)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="creator_sub_tasks", on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
	    return self.title
 
 
 
class TaskRecord(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="creator_task_records", on_delete=models.CASCADE)
    task = models.ForeignKey(SubTask, related_name='task_records', on_delete=models.CASCADE)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
	    return self.task.title    
