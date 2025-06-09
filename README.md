# To-Do List with Calendar Integration & Reminders

A simple to-do list application enhanced with a calendar view and automatic deadline reminders.

## Features

- Calendar integration to display tasks by date
- Email or SMS reminders for upcoming deadlines
- Toggle between list and calendar views

## Technologies Used

- Calendar library
- Notification service (SMTP)
- Backend framework (Flask, Django)

## Learning Highlights

- Calendar UI integration
- Time-based notifications
- Using third-party APIs

## Tutorial

### We do exactly like the checklist for using django channels
#### the Checklist
- ✔️	Install channels
- ✔️	Set ASGI_APPLICATION in settings.py
- ✔️	Configure CHANNEL_LAYERS
- ✔️	Create asgi.py with ProtocolTypeRouter
- ✔️	Add routing.py in your app with websocket_urlpatterns
- ✔️	Create AsyncWebsocketConsumer
- ✔️	Trigger updates via channel_layer.group_send
- ✔️	Add WebSocket connection JS in template
- ✔️	Run server with daphne (or uvicorn)


1. Install Requirements
```shell
pip install channels
```

2. Update settings.py
```python
# Enable ASGI
ASGI_APPLICATION = 'toDoList.asgi.application'


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}
```

3. Create asgi.py In your project root (beside settings.py):
```python
import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
import shared_tasks.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'toDoList.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            shared_tasks.routing.websocket_urlpatterns
        )
    ),
})
```

4. Create routing.py in your app
```python
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/shared-tasks/', consumers.SharedTaskConsumers.as_asgi()),
]
```

5. Create the WebSocket Consumer
```python
from channels.generic.websocket import AsyncJsonWebsocketConsumer

class SharedTaskConsumers(AsyncJsonWebsocketConsumer):

    async def connect(self):
        await self.channel_layer.group_add("shared_tasks", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("shared_tasks", self.channel_name)

    async def task_update(self, event):
        # Build a payload containing only the keys that actually exist
        payload = {
            "type": "task_update",
            "task_id": event["task_id"],
            "task_title": event["task_title"],
        }
        if "task_description" in event:
            payload["task_description"] = event["task_description"]
        if "task_completed" in event:
            payload["task_completed"] = event["task_completed"]

        await self.send_json(payload)
```

6. Trigger Events from Django Views
```python
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class SharedSubTaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = SubTask
    form_class = SubTaskForm
    template_name = "shared_task/shared_subtask_update.html"
    success_url = reverse_lazy('shared_task:shared_task_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        subtask = form.instance

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "shared_tasks",
            {
                "type": "task_update",
                "task_id": subtask.id,
                "task_title": subtask.title,
                "task_description": subtask.description,
                "task_completed": subtask.completed,
            }
        )
        return response
```

7. Frontend JavaScript WebSocket
```html
  <script>
    console.log(">>> live-update script running");
    const socket = new WebSocket('ws://' + window.location.host + '/ws/shared-tasks/');

    socket.onopen = () => console.log(">>> WebSocket onopen");
    socket.onerror = e => console.error(">>> WebSocket error", e);
    socket.onclose = () => console.warn(">>> WebSocket closed");

    socket.onmessage = function(e) {
      console.log(">>> onmessage got:", e.data);
      const data = JSON.parse(e.data);

      if (data.type === "task_update") {
        const id = data.task_id;
        const newTitle = data.task_title;
        const newDesc = data.task_description;
        const completed = data.task_completed;

        const container = document.querySelector(`#task-${id}`);
        if (!container) {
          console.log("No element with id=task-" + id);
          return;
        }

        // Update status badge
        const statusEl = container.querySelector(".subtask-status");
        if (statusEl) {
          if (completed) {
            statusEl.innerHTML = '<span class="badge bg-success">Finished</span>';
          } else {
            statusEl.innerHTML = '<span class="badge bg-secondary">Unfinished</span>';
          }
        }

        // Update title and description
        const titleEl = container.querySelector(".subtask-title");
        if (titleEl) {
          titleEl.textContent = newTitle;
        }
        const descEl = container.querySelector(".subtask-desc");
        if (descEl) {
          descEl.textContent = newDesc;
        }
        // Buttons remain unchanged
      }
    };
  </script>
```

8. Run Your App with Daphne
```shell
daphne -b 127.0.0.1 -p 8000 toDoList.asgi:application
```

- FINISHED