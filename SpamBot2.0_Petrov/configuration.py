from python_socks import ProxyType
 
API_ID = ""
API_HASH = ''

proxy = {
        'proxy_type': ProxyType.SOCKS5,
        'addr': "45.56.124.180",
        'port': 27614,
        'username': "modeler_2B6ifs",
        'password': "aNIxmx0U6huI",
        'rdns': True
    }

telegram_nicknames = [
    "Чатозавр",
    "Телеграмбуфер",
    "Стикерист",
    "Рассветчик",
    "Мемолог",
    "Гифоман",
    "Селфифейс",
    "Зависайчик",
    "Групоняша",
    "Комментарийчик",
    "Чатодром",
    "Флудонавт",
]

#{"api_id": "", "api_hash": "", "session": "", "phone_number": "", "name": ""}
accounts = [
    {"api_id": "", "api_hash": "", "session": "main_bot", "phone_number": "", "name": "Den4ik"},
    {"api_id": "", "api_hash": "", "session": "telethon1", "phone_number": "+27718504860", "name": "Den4ik_2"}
    
] 

photos = ['/Users/zgutadenis/Desktop/Work/SpamBot2.0_Petrov/1.jpeg',
          '/Users/zgutadenis/Desktop/Work/SpamBot2.0_Petrov/2.jpeg'
        ]

CONFIGURATION = {
    'DB_HOST' : 'localhost',
    'DB_USER' : 'root',
    'DB_NAME' : 'user_ids_db',
    'DB_PASSWORD' : 'root1234',
    'SENDER_EMAIL' : '',
    'APP_PASSWORD' : '',
    'API_TOKEN' : ''
}

STRUCTURED_MESSAGE = """
    <b>👤 Профіль</b>

    <b>👀 Ім'я: {name}</b>
    <b>🎒 Сесія: {session}</b>
    <b>📆 Номер: {phone_number}</b>
        """
