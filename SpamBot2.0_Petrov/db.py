import aiomysql
from configuration import *
from datetime import datetime
from email.message import EmailMessage
from aiosmtplib import SMTP
from datetime import datetime
import aiogram
from aiogram import types, Bot, Dispatcher, executor

async def connect_to_db():
    try:
        conn = await aiomysql.connect(
            host=CONFIGURATION['DB_HOST'],
            port=3306,
            user=CONFIGURATION['DB_USER'],
            password=CONFIGURATION['DB_PASSWORD'],
            db=CONFIGURATION['DB_NAME'],
            cursorclass=aiomysql.DictCursor)
    
        print("Connected successfully...")
        return conn
     
    except Exception as ex:
        print("Connection to DataBase refused...")
        print(ex)
        

async def add_id(user_id):
    conn = await connect_to_db()
    async with conn.cursor() as cursor:
        select_query = "SELECT username FROM user_ids WHERE username = %s"
        await cursor.execute(select_query, (user_id,))
        result = await cursor.fetchone()

        if result is None:
            insert_query = "INSERT INTO user_ids (username) VALUES (%s)"
            await cursor.execute(insert_query, (user_id,))
            await conn.commit()
        else:
            print(f"{user_id} already added to the Database!")
    
    conn.close()


async def get_non_processed_users():
    conn = await connect_to_db()
    async with conn.cursor() as cursor:
        select_query = "SELECT username FROM user_ids WHERE status = 0"
        await cursor.execute(select_query)
        result = await cursor.fetchall()
    
    if result:
        return result


async def send_message_to_user(user_id):
    conn = await connect_to_db()
    async with conn.cursor() as cursor:
        try:
            update_query = "UPDATE user_ids SET status = 1 WHERE username = %s"
            await cursor.execute(update_query, (user_id,))
            await conn.commit()
    
        except Exception as e:
            print(f"Error sending message to user with user_id {user_id}: {e}")

    conn.close()

async def database_check(choice: str):
    conn = await connect_to_db()
    async with conn.cursor() as cursor:
        if choice == "all":
            select_query = "SELECT * FROM user_ids"
        elif choice == "processed":
            select_query = "SELECT * FROM user_ids WHERE status = 1"
        elif choice == "notprocessed":
            select_query = "SELECT * FROM user_ids WHERE status = 0"
            
        await cursor.execute(select_query)
        result = await cursor.fetchall()
        
        if result:
            return result
        else:
            return None
    

async def user_announcement(announcement_type: str, time: str, error_message: str):
    if announcement_type == "turn_off":
        message = f'''
            <div class="container">
                <div class="announcement">Обов'язкове оповіщення!</div>
                <p>Шановний користувач,</p>
                <p>Бот @stonehaven_bot тимчасово вимкнуто.</p>
                <p>Дата та час вимкнення: {time}</p>
                <p>З повагою, Денчік-гореайтішнік.</p>
            </div>
            '''
    elif announcement_type == "error":
        message = f'''
            <div class="container">
                <div class="announcement">Помилка в роботі бота!</div>
                <p>Шановний користувач,</p>
                <p>Виникла помилка в роботі бота:</p>
                <p>{error_message}</p>
                <p>Дата та час помилки: {time}</p>
                <p>З повагою, Денчік-гореайтішнік.</p>
            </div>
            '''
    
    html = f'''
        <html>
        <head>
        <style>
            .container {{
            max-width: 500px;
            margin: 0 auto;
            background-color: #f1f1f1;
            border-radius: 10px;
            padding: 20px;
            }}

            .announcement {{
            background-color: #FF5733;
            color: #ffffff;
            font-weight: bold;
            font-size: 20px;
            text-align: center;
            padding: 20px;
            border-radius: 10px;
            }}

            @media only screen and (max-width: 600px) {{
            .container {{
                max-width: 100%;
            }}
            }}
        </style>
        </head>
        <body>
        {message}
        </body>
        </html>
        '''

    msg = EmailMessage()
    if announcement_type == "turn_off":
        msg['Subject'] = 'Bot-spammer | Оповіщення про вимкнення!'
    elif announcement_type == "error":
        msg['Subject'] = 'Bot-spammer | Помилка в роботі!'
    msg['From'] = CONFIGURATION['SENDER_EMAIL']
    msg['To'] = "denis.zhhuta@gmail.com"
    msg.set_content(html, subtype='html')

    async with SMTP(hostname='smtp.gmail.com', port=587, start_tls=True,
                    username=CONFIGURATION['SENDER_EMAIL'], password=CONFIGURATION['APP_PASSWORD']) as smtp:
        await smtp.send_message(msg)
