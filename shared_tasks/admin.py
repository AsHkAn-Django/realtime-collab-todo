from django.contrib import admin
from .models import SharedTask, SubTask, TaskRecord, ParticipationRequest

admin.site.register(SharedTask)
admin.site.register(SubTask)
admin.site.register(TaskRecord)
admin.site.register(ParticipationRequest)

