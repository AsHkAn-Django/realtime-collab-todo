from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

        

class SharedTask(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, through='ParticipationRequest', related_name='participating_tasks')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    
    @property
    def accepted_participants(self):
        return get_user_model().objects.filter(user_requests__task=self, user_requests__status='ACC')
    
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



class ParticipationRequest(models.Model):
    
    class Status(models.TextChoices):
        ACCEPTED = 'ACC', 'Accept'
        PENDING = 'PEN', 'Pending'
        REFUSED = 'REF', 'Refused'
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="user_requests", on_delete=models.CASCADE)
    task = models.ForeignKey(SharedTask, related_name='task_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=3, choices=Status.choices, default=Status.PENDING)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'task'], name='unique_user_request')
        ]

    def __str__(self):
        return f'{self.user.username} requested for {self.task.title}'
    
    def accept(self):
        self.status = self.Status.ACCEPTED
        self.save()
        
    def refuse(self):
        self.status = self.Status.REFUSED
        self.save()