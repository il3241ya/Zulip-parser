import zulip # Модуль для выполнения запросов к Zulip API


def client_authentication(path_tp_conf):
    """
    Функция выполняет аутентификацию пользователя в Zulip API на основе файла конфигурации.

    Параметры:
    path_tp_conf (str): Путь к файлу конфигурации Zulip, который содержит информацию
                       о пользователе, необходимую для аутентификации.

    Возвращает:
    zulip.Client: Объект клиента Zulip, представляющий аутентифицированное соединение с Zulip API.
    """
    client = zulip.Client(config_file=path_tp_conf)
    return client
