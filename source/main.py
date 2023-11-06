import time  # Модуль для работы с временем
import schedule  # Модуль для настройки и работы с переодичными задачами
import extractor
import auth
import zulip_requests
import bd_com
import config


START_FLAG = True
last_chat_data_list = []
last_message_data_list = []
last_subscribers_data_list = []


def periodic_task():
    """
    Функция, выполняющая периодическую задачу.

    Функция обращается к Zulip API, преобразует данные и сохраняет их в базу данных.
    """
    global START_FLAG
    global last_chat_data_list
    global last_message_data_list

    # Параметры подключения к базе данных ClickHouse
    db_host = config.Config.db_host 
    db_port = config.Config.db_port 

    # Параметры для запроса к чату
    operator = config.Config.operator 
    chat = config.Config.chat 

    # Запрос к Zulip API для получения сообщений в указанном чате
    zulip_response_chat = zulip_requests.request_for_mes_chat(zulip_client, operator, chat)

    # Запрос к Zulip API для получения списка подписчиков чата
    zulip_response_sub = zulip_requests.request_for_subscribers(zulip_client, chat)

    # Запрос к Zulip API для получения информации о пользователях
    zulip_response_users = zulip_requests.request_for_all_users(zulip_client)

    # Извлечение данных из ответа от Zulip
    chat_data = extractor.extraction_chat_inf(zulip_response_chat)
    message_data = extractor.extraction_message_inf(zulip_response_chat)

    subscribers_data = extractor.extraction_users_inf(zulip_response_sub, zulip_response_users)

    if START_FLAG:
        # Создание таблицы в базе данных ClickHouse при первом запуске
        bd_com.create_db(chat_data, message_data, subscribers_data, db_host, db_port)
        last_chat_data_list = chat_data
        last_message_data_list = message_data
        last_subscribers_data_list = subscribers_data
        START_FLAG = False

    elif (last_chat_data_list != chat_data or
          last_message_data_list != message_data or
          last_subscribers_data_list != subscribers_data):
        # Удаление и создание таблицы в базе данных при изменении данных
        bd_com.drop_tables()
        bd_com.create_db(chat_data, message_data, subscribers_data, db_host, db_port)
        last_chat_data_list = chat_data
        last_message_data_list = message_data
        last_subscribers_data_list = subscribers_data


if __name__ == "__main__":
    # Аутентификация в Zulip
    zulip_client = auth.client_authentication(config.Config.zulip_auth)

    # Запуск периодической задачи каждые 3 секунды
    schedule.every(3).seconds.do(periodic_task)
    while 1:
        schedule.run_pending()
        time.sleep(1)
