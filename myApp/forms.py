from django import forms
from .models import Task, Category

class CategoryForm(forms.ModelForm):
	class Meta:
		model = Category
		fields = ('title',)


class TaskForm(forms.ModelForm):
    # start with an empty queryset
    category = forms.ModelChoiceField(
        queryset=Category.objects.none(),
        widget=forms.RadioSelect,
        required=True,
    )

    class Meta:
        model = Task
        fields = ['category', 'title', 'description', 'deadline', 'priority']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(owner=user)
        
        
    
class FilterForm(forms.Form):
	category = forms.ChoiceField(widget=forms.RadioSelect, required=False)
	priority = forms.ChoiceField(widget=forms.RadioSelect, choices=Task.PRIORITY_CHOICES, required=False)
	
	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user')
		super().__init__(*args, **kwargs)
		self.fields['category'].choices = [(c.id, c.title) for c in Category.objects.filter(owner=user)]
	