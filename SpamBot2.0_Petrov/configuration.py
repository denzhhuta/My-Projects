from python_socks import ProxyType
 
API_ID = "20600849"
API_HASH = '41b4269e451bb95f0a2bfdd61d52947e'

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
    {"api_id": "20600849", "api_hash": "41b4269e451bb95f0a2bfdd61d52947e", "session": "main_bot", "phone_number": "+4915161584488", "name": "Den4ik"},
    {"api_id": "20600849", "api_hash": "41b4269e451bb95f0a2bfdd61d52947e", "session": "telethon1", "phone_number": "+27718504860", "name": "Den4ik_2"}
    
] 

photos = ['/Users/zgutadenis/Desktop/Work/SpamBot2.0_Petrov/1.jpeg',
          '/Users/zgutadenis/Desktop/Work/SpamBot2.0_Petrov/2.jpeg'
        ]

CONFIGURATION = {
    'DB_HOST' : 'localhost',
    'DB_USER' : 'root',
    'DB_NAME' : 'user_ids_db',
    'DB_PASSWORD' : 'root1234',
    'SENDER_EMAIL' : 'stonehaven.reset@gmail.com',
    'APP_PASSWORD' : 'lfemarbsgejrcfmq',
    'API_TOKEN' : '6053384973:AAHGLLvlUiz2bekhT5d9MAQoDV8zUTZ2C2Y'
}

STRUCTURED_MESSAGE = """
    <b>👤 Профіль</b>

    <b>👀 Ім'я: {name}</b>
    <b>🎒 Сесія: {session}</b>
    <b>📆 Номер: {phone_number}</b>
        """