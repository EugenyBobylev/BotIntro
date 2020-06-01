chat_state_dict = {}


def get_chat_state(chat_id) -> str:
    if chat_id in chat_state_dict:
        return chat_state_dict[chat_id]
    else:
        return ""


def set_chat_state(chat_id, value: str):
    chat_state_dict[chat_id] = value
