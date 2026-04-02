from cachetools import TTLCache

user_cache = TTLCache(maxsize=1000, ttl=24*3600) # 24h

def get_user_name(vk, user_id) -> str:
    try:
        if user_id in user_cache:
            return user_cache[user_id]

        user_info = vk.users.get(user_ids=user_id)[0] 
        full_name = f"{user_info['first_name']} {user_info['last_name']}"
        
        user_cache[user_id] = full_name
        return full_name
    except Exception as e:
        print(f"[ERROR] Произошла ошибка при получении имени для id{user_id}:")
        return ""