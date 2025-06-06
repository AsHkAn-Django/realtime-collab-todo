# shared_tasks/consumers.py

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
