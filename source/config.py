class Config:
    # Параметры подключения к базе данных ClickHouse
    db_host = 'my-clickhouse'
    db_port = 8123

    # Параметры авторизации Zulip
    zulip_auth = "../zulip_config/.zuliprc"

    # Параметры для запроса к чату
    operator = 'stream'
    chat = "Проектный офис"


