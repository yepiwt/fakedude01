import confs
from loguru import logger
from aiogram.types import Message
from aiogram import Dispatcher

CONFIG_OBJ = None
VK_BOT = None

def config_tg_hand(c = None):
	global CONFIG_OBJ
	if not c:
		return CONFIG_OBJ
	CONFIG_OBJ = c

def setup_vk_bot_to_tg_handler(bot):
	global VK_BOT
	VK_BOT = bot

async def start_cmd(msg: Message):
	logger.info(f"{msg.from_user.full_name} send /start")
	await msg.answer("Basic reply")

async def help(msg: Message):
	logger.info(f"{msg.from_user.full_name} send /help")
	await msg.answer('This is gate')

async def notif(msg: Message):
	global CONFIG_OBJ
	args = msg.text.split(' ') # args = ['/notif', 'id']
	if len(args) != 1:
		if args[1] == 'me':
			answer = f"Changed notificator id: {str(CONFIG_OBJ['tg']['notificate_to'])} ---> {msg.from_user.id}"
			logger.debug(f'{msg.from_user.id}: {answer}')
			CONFIG_OBJ['tg']['notificate_to'] = msg.from_user.id
			await msg.answer(answer)
		else:
			try:
				new_notif = int(args[1])
			except:
				await msg.answer('bad syntax')
			else:
				answer = f"Changed: {str(CONFIG_OBJ['tg']['notificate_to'])} ---> {new_notif}"
				await msg.answer(answer)
				logger.debug(f'{msg.from_user.id}: {answer}')
				CONFIG_OBJ['tg']['notificate_to'] = new_notif
	else:
		await msg.answer(str(CONFIG_OBJ['tg']['notificate_to']))

async def vk_hand(msg: Message):
	global CONFIG_OBJ, VK_BOT
	args = msg.text.split(' ')
	if len(args) == 1:
		await msg.answer('ne robit')
	elif args[1] == 'chats':
		answ = ''
		for n,chat in enumerate(CONFIG_OBJ['vk']['chats']):
			answ += f'{n}: {chat}'
		await msg.answer(answ or 'no them')
	elif args[1] == 'convs':
		answ = ''
		n = []
		result = await VK_BOT.api_context.messages.get_conversations()
		for conv in result.response.items:
			result2 = await VK_BOT.api_context.users.get(user_ids=conv.conversation.peer.id, fields='first_name,last_name')
			f,l = result2.response[0].first_name,result2.response[0].last_name
			n.append([conv.conversation.peer.id,f,l])
		krasivaya_stroka = ""
		for i,man in enumerate(n):
			krasivaya_stroka += f'{i+1}. {man[1]} {man[2]}\n'
		await msg.answer(krasivaya_stroka or 'nothing')
	elif args[1] == 'conv':
		pass
	elif args[1] == 'chat':
		pass
	else:
		await msg.answer('bad syntax')

async def anything(msg: Message):
	logger.info(f"{msg.from_user.full_name} send something. {msg['from']['id']} idk")
	if msg.chat.id > 0:
		logger.debug('licnoe')
	else:
		logger.debug('iz besedi')
	await msg.answer(msg.text)

def setup_tg_handlers(dp: Dispatcher):
	dp.register_message_handler(start_cmd, commands=['start'])
	dp.register_message_handler(help, commands=['help'])
	dp.register_message_handler(notif, commands=['notif'])
	dp.register_message_handler(vk_hand, commands=['v'])
	dp.register_message_handler(anything)