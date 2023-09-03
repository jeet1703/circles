import json
from time import sleep
from channels.generic.websocket import AsyncWebsocketConsumer, StopConsumer
from main.models import User, Circle, Conversation, Message, Server
from django.contrib.auth.hashers import check_password
from channels.db import database_sync_to_async


class MainConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        
        await self.accept()
        print("Connected")

        if await self.check_user():
            print("User is ok!")

            location = await self.get_location()
            position = await self.get_position()

            initial_message = {
                "type": "initial_message",
                "username": self.username,
                "location_server": location[0],
                "location_circle": location[1],
                "x": position[0],
                "y": position[1],
            }

            await self.send(json.dumps(initial_message))

        else:
            self.close()

    async def disconnect(self, close_code):
        print("disconnected")
        pass

    async def receive(self, text_data):
        print(text_data)
        await self.send(text_data)

    @database_sync_to_async
    def check_user(self):

        username = self.scope["session"]["username"]
        password = self.scope["session"]["password"]

        self.username = username
        self.password = password

        user = User.objects.filter(username=username)

        if len(user) == 1:
            if check_password(password, user[0].password):
                print("Logged in")
                return True

            else:
                return False

        elif len(user) > 1:
            return False

        elif len(user) == 0:
            return False
        
    @database_sync_to_async
    def get_position(self):

        user = User.objects.filter(username=self.username)[0]
        return [user.x, user.y]
    
    @database_sync_to_async
    def get_location(self):
        
        user = User.objects.filter(username=self.username)[0]
        return [user.location_server, user.location_circle]
        
        