def request_for_all_users(client):
    """
    Выполняет запрос к Zulip API для получения списка всех пользователей.

    Параметры:
    client (ZulipClient): Клиент Zulip для выполнения запроса.

    Возвращает:
    dict: Результат запроса, содержащий список пользователей.
    """
    result = client.get_members()
    return result


def request_for_mes_chat(client, operator, chat):
    """
    Выполняет запрос к Zulip API для получения сообщений в указанном чате.

    Параметры:
    client (ZulipClient): Клиент Zulip для выполнения запроса.
    operator (str): Оператор (например, "stream" или "sender").
    chat (str): Имя чата или email пользователя.

    Возвращает:
    dict: Результат запроса, содержащий сообщения в указанном чате.
    """
    request = {
    "anchor": "newest",
    "num_before": 1000,
    "num_after": 0,
    "narrow": [
            {
                "operator": operator,
                "operand": chat
            }
            ]
    }
    result = client.get_messages(request)
    return result


def request_for_subscribers(client, chat):
    """
    Выполняет запрос к Zulip API для получения подписчиков указанного чата.

    Параметры:
    client (ZulipClient): Клиент Zulip для выполнения запроса.
    chat (str): Имя чата.

    Возвращает:
    dict: Результат запроса, содержащий список id подписчиков чата.
    """
    result = client.get_subscribers(stream=chat)
    return result
