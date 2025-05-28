from django import forms
from .models import Task, Category

class CategoryForm(forms.ModelForm):
	class Meta:
		model = Category
		fields = '__all__'


class TaskForm(forms.ModelForm):
	class Meta:
		model = Task
		fields = ['category', 'title', 'description', 'deadline', 'priority']
		widgets = {
			'deadline': forms.DateInput(attrs={'type': 'date'}),
		}

    
class FilterForm(forms.Form):
	category = forms.ChoiceField(widget=forms.RadioSelect, required=False)
	priority = forms.ChoiceField(widget=forms.RadioSelect, choices=Task.PRIORITY_CHOICES, required=False)
 
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['category'].choices = [(c.id, c.title) for c in Category.objects.all()]
	