import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope['user'].is_authenticated:
            await self.channel_layer.group_add("dashboard", self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("dashboard", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        # Lógica de recebimento de dados

    async def alerta_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'novo_alerta',
            'alerta': event['alerta']
        }))