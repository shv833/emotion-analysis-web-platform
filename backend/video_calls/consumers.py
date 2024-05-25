import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from groups.models import Group, GroupStudent


class VideoCallConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_id = self.scope["url_route"]["kwargs"]["group_id"]
        self.room_group_name = f"videocall_{self.group_id}"

        if isinstance(self.scope["user"], AnonymousUser):
            await self.close()
        else:
            self.group = await self.get_group(self.group_id)
            if self.group and (
                await self.is_teacher(self.group, self.scope["user"])
                or await self.is_group_student(self.group, self.scope["user"])
            ):
                if self.channel_layer is not None:
                    await self.channel_layer.group_add(self.room_group_name, self.channel_name)
                    await self.accept()
                else:
                    await self.close()
            else:
                await self.close()

    async def disconnect(self, close_code):
        if self.channel_layer is not None:
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]

        if self.channel_layer is not None:
            await self.channel_layer.group_send(self.room_group_name, {"type": "chat_message", "message": message})

    async def chat_message(self, event):
        message = event["message"]

        await self.send(text_data=json.dumps({"message": message}))

    @database_sync_to_async
    def get_group(self, group_id):
        try:
            return Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return None

    @database_sync_to_async
    def is_group_student(self, group, user):
        return GroupStudent.objects.filter(group=group, student=user).exists()

    @database_sync_to_async
    def is_teacher(self, group, user):
        return group.teacher == user
