from celery import shared_task
from twilio.rest import Client
from django.conf import settings
from .models import Task


@shared_task
def send_alert_sms():
    client = Client(settings.MY_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    tasks = Task.objects.all()

    for task in tasks:
        message = f"Overdue Task!\nYour task '{task.title}' was due on {task.deadline}. Do it now!"
        
        if task.is_overdue():
            client.messages.create(
                to=settings.MY_PHONE_NUMBER,
                from_=settings.MY_TWILIO_NUMBER,
                body=message
            )
            print(f"✅ Sent SMS for task: {task.title}")
