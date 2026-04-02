import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import config
from gptunnel import GPTTunnel
from datetime import datetime
import utils

vk_session = vk_api.VkApi(token=config.vk_token)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, config.vk_bot_group_id)

gpt = GPTTunnel(config.gpttoken)

def is_triggered(msg) -> bool:
    is_conversation = msg.conversation_message_id
    if not is_conversation:
        return False

    if len(config.triggers) == 0:
        return True

    if any(trigger.lower() in msg.text.lower() for trigger in config.triggers):
        return True

    if not config.is_trigger_on_reply:
        return False

    reply = msg.get('reply_message')
        
    if reply:
        is_reply_to_bot = (reply['from_id'] == -config.vk_bot_group_id)
        if is_reply_to_bot:
            return True

    return False

while True:
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                msg = event.message


                try:
                    if not is_triggered(msg):
                        continue

                    # подпись 'печатает...'
                    vk.messages.setActivity(
                        type='typing', 
                        peer_id=msg.peer_id, 
                        group_id=config.vk_bot_group_id
                    )

                    user_id = msg.from_id
                    user_name = utils.get_user_name(vk, user_id)

                    result = gpt.askAssistant('mdpakhmurin-assistant-ai6495591', 'ai6495591', msg.text + "\n" + "отправитель:" + user_name)
                    raw_answer: str = result["message"]

                    vk.messages.send(
                        peer_id=msg.peer_id,
                        random_id=0,
                        message=raw_answer,
                        forward=f'{{"peer_id": {msg.peer_id}, "conversation_message_ids": [{msg.conversation_message_id}], "is_reply": true}}'
                    )
                        
                except Exception as e:
                    print(datetime.now(), "\t", "error filtering message:", e)

    except Exception as e:
        print(datetime.now(), "\t", "Unexpected error:", e)
        time.sleep(20)
        continue