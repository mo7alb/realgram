import json

from channels.generic.websocket import WebsocketConsumer
from apps.message.models import Message

class ChatConsumer(WebsocketConsumer):
	def connect(self):
		''' Decide what to do when a user connects '''
		self.accept()
	
	def connect(self, close_code):
		''' Decide what to do when a user disconnects '''
		print('user left')

	def receive(self, text_data=None):
		load_data = json.loads(text_data)
		message = load_data['message']
		slug = load_data['slug']
		profile_id = load_data['profileId']

		Message.objects.create(
			message=message,
			slug=slug,
			reciever=profile_id
		)

		self.send(text_data=json.dumps({ 'message': message }))