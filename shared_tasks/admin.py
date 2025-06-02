from django.contrib import admin
from .models import SharedTask, SubTask, TaskRecord, ParticipationRequest


class ParticipationRequestInline(admin.TabularInline):
    model = ParticipationRequest
    extra = 0
    readonly_fields = ['user', 'status', 'created']
    
    
@admin.register(SharedTask)
class SharedTaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'creator', 'completed', 'created']
    inlines = [ParticipationRequestInline]   
    

admin.site.register(SubTask)
admin.site.register(TaskRecord)
admin.site.register(ParticipationRequest)

