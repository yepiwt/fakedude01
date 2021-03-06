from vkwave.bots import SimpleLongPollBot
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from loguru import logger
import asyncio

import confs
c = confs.Config()
if not c.data:
	new_passw = input('Введите новый пароль для конфига: ')
	new_vk_token = input('Введите вк токен: ')
	new_group_id = input('Введите вк айди группы: ')
	new_tg_token = input('Введите тг-бот токен: ')
	c.new_cfg(new_passw,new_vk_token,new_group_id,new_tg_token)
else:
	passw = input('Введите пароль от конфига:') # passw = 123
	c.unlock_file(passw)

logger.info('Started')

bot = Bot(token=c.data['tg']['token'])
dp = Dispatcher(bot)
logger.debug('Telegram: got api')

vk_bot = SimpleLongPollBot(tokens=c.data['vk']['public_token'], group_id=c.data['vk']['public_id'])
logger.debug('VKAPI: registered bot')

import handlers

# Telegram
handlers.setup_tg_handlers(dp)
handlers.config_tg_hand(c.data)
handlers.setup_tg_api(bot)
handlers.setup_vk_bot_to_tg_handler(vk_bot)
logger.debug('Telegram: ready')

# Vkontakte
handlers.setup_tg_bot_to_vk_handler(bot)
handlers.config_vk_hand(c.data)
vk_bot.dispatcher.add_router(handlers.vk_msg_from_chat)
logger.debug('VKAPI: ready')

async def start_polling_vk():
    await vk_bot.run()
    logger.debug('Polling Vk')

dp.loop.create_task(start_polling_vk())
logger.debug('Polling Telegram')
executor.start_polling(dp, skip_updates=True)

#Do after closing
c.data = handlers.config_tg_hand()
c.data['vk']['chats'] = handlers.config_vk_hand()['vk']['chats']
c.save_in_file()