import json
from channels.generic.websocket import AsyncWebsocketConsumer

class SeatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.theater_id = self.scope['url_route']['kwargs']['theater_id']
        self.group_name = f"theater_{self.theater_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def seat_update(self, event):
        await self.send(text_data=json.dumps({
            "seats": event["seats"]
        }))
