from django import forms
from .models import TaskRecord, SubTask, SharedTask



class ShareTaskForm(forms.ModelForm):
    
    class Meta:
        model = SharedTask
        fields = ['title', 'description',]
        

class SubTaskForm(forms.ModelForm):
    
    class Meta:
        model = SubTask
        fields = ['title', 'description',]
        
        
class TaskRecordForm(forms.ModelForm):
    
    class Meta:
        model = TaskRecord
        fields = ['description',]