import aiomysql
import asyncio
import string
from email.message import EmailMessage
from aiosmtplib import SMTP
from datetime import datetime
from configuration import CONFIGURATION

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

async def add_post_to_database(post_id: int):
    conn = await connect_to_db()
    async with conn.cursor() as cursor:
        select_query = "SELECT message_id FROM message_schedule WHERE message_id = %s"
        await cursor.execute(select_query, (post_id,))
        result = await cursor.fetchone()
        
        if result is None:
            post_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            insert_query = "INSERT INTO message_schedule (message_id, approval_date) VALUES (%s, %s)"
            await cursor.execute(insert_query, (post_id, post_date))
            await conn.commit()
            conn.close()

            return "<b>✅ Успішно додано до черги!</b>"
        
        else:
            pass
            return "<b>😔 Цей пост вже одобрено!</b>"
    

async def post_sender():
    conn = await connect_to_db()
    async with conn.cursor() as cursor:
        select_query = "SELECT * FROM message_schedule WHERE sent_status = 0 ORDER BY approval_date LIMIT 1"
        await cursor.execute(select_query)
        row = await cursor.fetchone()
                
        if row:
            try:
                insert_query = "UPDATE message_schedule SET sent_status = 1 WHERE id = %s"
                await cursor.execute(insert_query, (row['id'],))
                await conn.commit()
        
                return row['message_id'] 
            except Exception as ex:
                print("ERROR")       

async def database_check(choice: str):
    conn = await connect_to_db()
    async with conn.cursor() as cursor:
        if choice == "all":
            select_query = "SELECT * FROM message_schedule"
        elif choice == "processed":
            select_query = "SELECT * FROM message_schedule WHERE sent_status = 1"
        elif choice == "notprocessed":
            select_query = "SELECT * FROM message_schedule WHERE sent_status = 0"
            
        await cursor.execute(select_query)
        result = await cursor.fetchall()
        
        if result:
            return result
        else:
            return None
        

async def db_cleaner():
    conn = await connect_to_db()
    async with conn.cursor() as cursor:
        select_query = "SELECT * FROM message_schedule WHERE sent_status = 1"
        await cursor.execute(select_query)
        count = await cursor.fetchall()
        
        if count:
                try:
                    insert_query = "DELETE FROM message_schedule WHERE sent_status = 1"
                    await cursor.execute(insert_query)
                    await conn.commit()
                    
                    return count
                
                except Exception as ex:
                    print("Unknown error with function db_cleaner. Maybe there are no messages to delete. Check Database manually!")
        
        else:
            return "<b>😔 Помилка! Мабудь, нічого видаляти?</b>"
    
    conn.close()
                
      
async def user_announcement(announcement_type: str, time: str, error_message: str):
    if announcement_type == "turn_off":
        message = f'''
            <div class="container">
                <div class="announcement">Обов'язкове оповіщення!</div>
                <p>Шановний користувач,</p>
                <p>Бот @copycatpetrov_bot тимчасово вимкнуто.</p>
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
        msg['Subject'] = 'Bot-copy | Оповіщення про вимкнення!'
    elif announcement_type == "error":
        msg['Subject'] = 'Bot-copy | Помилка в роботі!'
    msg['From'] = CONFIGURATION['SENDER_EMAIL']
    msg['To'] = "denis.zhhuta@gmail.com"
    msg.set_content(html, subtype='html')

    async with SMTP(hostname='smtp.gmail.com', port=587, start_tls=True,
                    username=CONFIGURATION['SENDER_EMAIL'], password=CONFIGURATION['APP_PASSWORD']) as smtp:
        await smtp.send_message(msg)
