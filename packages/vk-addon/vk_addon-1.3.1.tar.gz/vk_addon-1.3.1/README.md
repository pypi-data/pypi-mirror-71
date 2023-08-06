# Что это?

Это библиотека, созданая для помощи работы с vk_api. 

В нее входят новые методы: `message_new`, `chat_invite_user`, `chat_kick_user`, `chat_invite_by_link` и т.д.

# Установка VkAddon

	```sh
	pip install vk_addon
	```

# Работа с VkAddon

Для работы нужно импортировать библиотеку и подключить ее в своего бота

	```py
	import vk_api, vk_addon
	from vk_addon.get_random_id import random_id
	from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll

	vk_session = vk_api.VkApi(token='Ваш токен')
	vk = vk_session.get_api()
	longpoll = VkBotLongPoll(vk_session, ID сообщества)	

	while True:
		for event in longpoll.listen()
			bot = vk_addon.VkAddon(event=event.raw) # Подключения библиотеки VkAddon

			if bot.type() == 'message_new': #Проверка на тип действия. В нашем случае - message_new
				vk.messages.send(peer_id=bot.peer_id(), message=bot.text(), random_id=random_id()) # bot.text() - сообщение

			elif bot.type() == 'chat_invite_user':
				vk.messages.send(peer_id=bot.peer_id(), message=f'[id{bot.member()}|Пользователь] вступил в беседу') # bot.member() - Пользователь, которого пригласили в беседу

# Проект не стоит на месте и работает дальше! Если нашли баги:

	VK: https://vk.com/fanepka
	Gmail: play.fanner@gmail.com
	Telegram: @fanepka
	Yandex: spickplay.mc@yandex.ru