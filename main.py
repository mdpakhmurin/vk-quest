import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import config

vk_session = vk_api.VkApi(token=config.vk_token)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, config.vk_bot_group_id)

while True:
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                msg = event.message

                print(msg)

                try:
                    is_conversation = msg.conversation_message_id
                    if not is_conversation:
                        continue

                    if not any(trigger in msg.text for trigger in config.triggers):
                        continue

                    # if (config.peer_ids 
                    #     and len(config.peer_ids) != 0 
                    #     and msg.peer_id not in config.peer_ids):
                    #     continue

                    vk.messages.send(
                        peer_id=msg.peer_id,
                        random_id=0,
                        message="пошел нахуй",
                        forward=f'{{"peer_id": {msg.peer_id}, "conversation_message_ids": [{msg.conversation_message_id}], "is_reply": true}}'
                    )
                        
                except Exception as e:
                    print(datetime.now(), "\t", "error filtering message:", e)

    except Exception as e:
        print(datetime.now(), "\t", "Unexpected error:", e)
        time.sleep(30)
        continue