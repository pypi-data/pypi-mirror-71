import vk_api

class VkAddonError(Exception):
	def __init__(self, text):
		self.text = text

class VkAddon:
	def __init__(self, event=None, on=True):
		self.event = event

	def connect(self):
		if self.event == None:
			raise VkAddonError('Не указан "event"')

		else:
			pass

	def type(self):
		try:
			if self.event['object']['from_id'] > 0:
				if self.event['object']['action']['type'] == 'chat_invite_user':
					return 'chat_invite_user'

				if self.event['object']['action']['type'] == 'chat_invite_user_by_link':
					return 'chat_invite_user_by_link'

				elif self.event['object']['action']['type'] == 'chat_kick_user':
					return 'chat_kick_user'

				else:
					return self.event['object']['action']['type']

		except KeyError:
			if self.event['type'] == 'message_new':				
				return 'message_new'

			elif self.event['type'] == 'message_typing_state':
				return 'message_typing_state'


	def member(self):
		return self.event['object']['action']['member_id']

	def from_id(self):
		return self.event['object']['from_id']

	def peer_id(self):
		return self.event['object']['peer_id']

	def text(self):
		return self.event['object']['text']



