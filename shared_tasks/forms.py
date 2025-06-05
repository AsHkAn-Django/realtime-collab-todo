from django import forms
from .models import TaskRecord, SubTask, SharedTask, ParticipationRequest



class ShareTaskForm(forms.ModelForm):
    
    class Meta:
        model = SharedTask
        fields = ['title', 'description',]
        

class SubTaskForm(forms.ModelForm):
    
    class Meta:
        model = SubTask
        fields = ['title', 'description', 'completed']
        
        
class TaskRecordForm(forms.ModelForm):
    
    class Meta:
        model = TaskRecord
        fields = ['description',]
        
        
class ParticipationRequestForm(forms.ModelForm):
    
    class Meta:
        model = ParticipationRequest
        fields = []