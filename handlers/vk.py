from vkwave.bots import DefaultRouter, SimpleBotEvent, simple_bot_message_handler
from vkwave.bots.core.dispatching import filters
from loguru import logger

vk_msg_from_chat = DefaultRouter()

tg_bot = None

def setup_tg_bot_to_vk_handler(new_global):
    global tg_bot
    tg_bot = new_global

@simple_bot_message_handler(vk_msg_from_chat,filters.MessageFromConversationTypeFilter("from_chat"))
async def answer_chat(event: SimpleBotEvent):
    global tg_bot
    usr_id = event.object.object.message.from_id #event.object.object.message.from_id
    answer = await event.api_ctx.users.get(user_ids=usr_id,fields='first_name,last_name')
    f,l = answer.response[0].first_name, answer.response[0].last_name
    notification_text = f'Сообщение из беседы от {f} {l}\n{event.object.object.message.text}'
    logger.debug(f'New message from VK: {f} {l}')
    await tg_bot.send_message("", notification_text)

@simple_bot_message_handler(vk_msg_from_chat,filters.MessageFromConversationTypeFilter("from_pm"))
async def answer_conv(event: SimpleBotEvent):
    global tg_bot
    usr_id = event.object.object.message.from_id #event.object.object.message.from_id
    answer = await event.api_ctx.users.get(user_ids=usr_id,fields='first_name,last_name')
    f,l = answer.response[0].first_name, answer.response[0].last_name
    notification_text = f'Личное сообщение от {f} {l}\n{event.object.object.message.text}'
    logger.debug(f'New message from VK: {f} {l}')
    await tg_bot.send_message("", notification_text)

#async tg_notification(id, )
