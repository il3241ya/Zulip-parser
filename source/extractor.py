def extraction_chat_inf(response):
    """
    Извлекает информацию о чате из ответа Zulip API.

    Параметры:
    response (dict): Ответ Zulip API.

    Возвращает:
    list: Список данных о чате в формате
    [chat_id, sender_id, message_id].
    """
    chat_data = []
    for message in response['messages']:
        chat_data.append([message['recipient_id'],
                          message['sender_id'],
                          message['id']])

    return chat_data


def extraction_message_inf(response):
    """
    Извлекает информацию о сообщениях из ответа Zulip API.

    Параметры:
    response (dict): Ответ Zulip API.

    Возвращает:
    list: Список данных о сообщениях в формате
    [message_id, message_content, message_subject, sender_id].
    """
    message_data = []
    for message in response['messages']:
        message_data.append([message['id'],
                             message['content'],
                             message['subject'],
                             message['sender_id']])

    return message_data


def extraction_users_inf(id_response, data_response):
    """
    Извлекает информацию о пользователях из ответов Zulip API.

    Параметры:
    id_response (dict): Ответ Zulip API с id подписчиков.
    data_response (dict): Ответ Zulip API с данными о пользователях.

    Возвращает:
    list: Список данных о пользователях в формате
    [user_id, email, full_name].
    """
    users_id = []

    sub_ids = id_response['subscribers']
    for sub_id in sub_ids:
        users_id.append(int(sub_id))

    users_data = [[member["user_id"],
                   member["email"],
                   member["full_name"]]
                   for member in data_response["members"] if member["user_id"] in users_id]

    return users_data
