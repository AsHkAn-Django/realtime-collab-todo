from django.db import models

from django.utils import timezone


class Category(models.Model):
	title = models.CharField(max_length=264)

	class Meta:
		verbose_name = 'Category'
		verbose_name_plural = 'Categories'

	def __str__(self):
		return self.title
  

class Task(models.Model):
	PRIORITY_CHOICES = [
	('0', 'No Priority'),
	('1', 'Normal'),
	('2', 'Important'),
	('3', 'Really Important'),
	]

	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='tasks')
	title = models.CharField(max_length=264)
	description = models.CharField(max_length=264, null=True, blank=True)
	deadline = models.DateTimeField()
	overdue = models.BooleanField(default=False)
	priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES)

	def __str__(self):
		return self.title

	def is_overdue(self):
		return self.deadline < timezone.now()
        

