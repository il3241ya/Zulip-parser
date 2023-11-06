import clickhouse_connect  # Модуль для подключения к бд clickhouse и выполнения запросов


def create_db(chat_data, 
              message_data,
              subscribers_data,
              db_host,
              db_port,
              tb_chat='chat',
              tb_mes='messages',
              tb_sub='subscribers'):
    """
    Создает базу данных ClickHouse и заполняет ее данными о чатах, сообщениях и подписчиках.

    Параметры:
    chat_data (list): Список данных о чатах.
    message_data (list): Список данных о сообщениях.
    subscribers_data (list): Список данных о подписчиках.
    db_host (str): Хост ClickHouse сервера.
    db_port (int): Порт ClickHouse сервера.
    tb_chat (str): Имя таблицы для данных о чатах.
    tb_mes (str): Имя таблицы для данных о сообщениях.
    tb_sub (str): Имя таблицы для данных о подписчиках.
    """
    create_chat_table(tb_chat, chat_data, db_host, db_port)
    create_messages_table(tb_mes, message_data, db_host, db_port)
    create_users_table(tb_sub, subscribers_data, db_host, db_port)


def create_chat_table(tb_name='chat',
                      data=[000, 000, 000],
                      db_host='my-clickhouse',
                      db_port=8123):
    """
    Создает таблицу в ClickHouse для хранения данных о чатах и заполняет ее данными.

    Параметры:
    tb_name (str): Имя таблицы.
    data (list): Список данных для заполнения таблицы.
    db_host (str): Хост ClickHouse сервера.
    db_port (int): Порт ClickHouse сервера.
    """
    sql_req = f"CREATE TABLE IF NOT EXISTS {tb_name} \
                (chat_id Int64, \
                 sender_id Int64, \
                 message_id Int64) ENGINE MergeTree \
                 ORDER BY chat_id"

    client = clickhouse_connect.get_client(host=db_host, port=db_port)
    client.command( sql_req)
    client.insert(tb_name, data, column_names=['chat_id',
                                               'sender_id',
                                               'message_id'])


def create_messages_table(tb_name='messages',
                          data=[000, "default_content", "default_subject", 000],
                          db_host='my-clickhouse',
                          db_port=8123):
    """
    Создает таблицу в ClickHouse для хранения данных о сообщениях и заполняет ее данными.

    Параметры:
    tb_name (str): Имя таблицы.
    data (list): Список данных для заполнения таблицы.
    db_host (str): Хост ClickHouse сервера.
    db_port (int): Порт ClickHouse сервера.
    """
    sql_req = f"CREATE TABLE IF NOT EXISTS {tb_name} \
                (message_id Int64, \
                 message_content String, \
                 message_subject String, \
                 sub_id Int64) ENGINE MergeTree \
                 ORDER BY message_id"

    client = clickhouse_connect.get_client(host=db_host, port=db_port)
    client.command(sql_req)
    client.insert(tb_name, data, column_names=['message_id',
                                               'message_content',
                                               'message_subject',
                                               'sub_id'])


def create_users_table(tb_name='subscribers',
                      data=[000, 'email_def', "fullname_def"],
                      db_host='my-clickhouse',
                      db_port=8123):
    """
    Создает таблицу в ClickHouse для хранения данных о подписчиках и заполняет ее данными.

    Параметры:
    tb_name (str): Имя таблицы.
    data (list): Список данных для заполнения таблицы.
    db_host (str): Хост ClickHouse сервера.
    db_port (int): Порт ClickHouse сервера.
    """
    sql_req = f"CREATE TABLE IF NOT EXISTS {tb_name} \
                (sub_id Int64, \
                email String, \
                full_name String) ENGINE MergeTree \
                ORDER BY sub_id"

    client = clickhouse_connect.get_client(host=db_host, port=db_port)
    client.command(sql_req)
    client.insert(tb_name, data, column_names=['sub_id',
                                               'email',
                                               'full_name'])


def drop_tables(db_chat='chat',
               db_mes='messages',
               db_users='subscribers',
               db_host='my-clickhouse',
               db_port=8123):
    """
    Удаляет указанные таблицы из ClickHouse, если они существуют.

    Параметры:
    db_chat (str): Имя таблицы для данных о чатах.
    db_mes (str): Имя таблицы для данных о сообщениях.
    db_users (str): Имя таблицы для данных о подписчиках.
    db_host (str): Хост ClickHouse сервера.
    db_port (int): Порт ClickHouse сервера.
    """
    client = clickhouse_connect.get_client(host=db_host, port=db_port)

    sql_req = f"DROP TABLE IF EXISTS {db_chat}"
    client.command(sql_req)

    sql_req = f"DROP TABLE IF EXISTS {db_mes}"
    client.command(sql_req)

    sql_req = f"DROP TABLE IF EXISTS {db_users}"
    client.command(sql_req)
