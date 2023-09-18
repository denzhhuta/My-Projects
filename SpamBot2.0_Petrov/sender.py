import telethon
import aiogram
from aiogram import types, Bot, Dispatcher, executor, filters
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telethon import TelegramClient, events
from telethon.errors.rpcerrorlist import PhoneNumberBannedError
from telethon.tl.types import PeerUser
from telethon.tl import types
from configuration import *
from keyboard import *
import random
import asyncio
import hashlib
from datetime import datetime
from db import *
import os
import sys
import csv

comments = []
comments_used = []



class CheckSubscriptionUserMiddleware(BaseMiddleware):
    def __init__(self):
         self.prefix = 'key_prefix'
         super(CheckSubscriptionUserMiddleware, self).__init__()
    
    async def on_process_update(self, update: types.Update, data: dict):
        if "message" in update:
            this_user = update.message.from_user
            if update.message.text:
                if "start" in update.message.text:
                    return
    
        elif "callback_query" in update:
            this_user = update.callback_query.from_user
        
        else:
            this_user = None
        
        if this_user is not None:
            get_prefix = self.prefix
                     
            if not this_user.is_bot:                       
                user_id = this_user.id
                if this_user.username != "morkovka2005" and this_user.username != "andrey_prac" and this_user.username != "auditoreold" and this_user.username != "YuliiaBuha":
                    await bot.send_message(user_id, "<b>😔 You are not allowed to use this bot!</b>", parse_mode="HTML") 
                    raise CancelHandler()  
                

with open('C:\\Users\\admin\\Desktop\\Spammer_2.0\\messages.csv', 'r', encoding='utf-8') as file:
    csvreader = csv.reader(file, delimiter='/')
    for row in csvreader:
        if row:
            message_text = row[0]
            comments.append(message_text.strip())
            
bot = aiogram.Bot(CONFIGURATION['API_TOKEN'])
storage = MemoryStorage()
dp = aiogram.Dispatcher(bot, storage=storage)

message_mapping = {}
client_lock = asyncio.Lock()
message_send = 0
message_failed = 0

async def generate_credentials_indentifier(session, phone_number, name):
    identifier_string = f"{session}{phone_number}{name}"
    identifier_hash = hashlib.md5(identifier_string.encode()).hexdigest()
    return identifier_hash


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message) -> None:
    last_name = message.from_user.last_name
    
    if last_name is None:
        await bot.send_message(chat_id=message.from_user.id,
                           text=f"<b>Привіт, {message.from_user.first_name}!</b>",
                           parse_mode="HTML",
                           reply_markup = main_reply_keyboard())
    else:
        await bot.send_message(chat_id=message.from_user.id,
                           text=f"<b>Привіт, {message.from_user.first_name} {message.from_user.last_name}!</b>",
                           parse_mode="HTML",
                           reply_markup = main_reply_keyboard())
        
@dp.message_handler(text='Почати розсилку 🧨')
async def send_start_handler(message: types.Message):
    global message_send, message_failed
    banned_accounts_count = set()
    problem_ids = []
    
    while len(banned_accounts_count) < len(accounts):
        random_account = random.choice(accounts)
        async with client_lock:
            client = TelegramClient(random_account['session'], random_account['api_id'], random_account['api_hash'], proxy=proxy)
            await client.connect()
            try:
                if not await client.is_user_authorized():
                        await client.send_code_request(phone=random_account['phone_number'])
                
                users = await get_non_processed_users()
                if not users:
                    await bot.send_message(chat_id=message.chat.id,
                                        text="<b>🤨 Пхд немає айдішніків в базі даних</b>",
                                        parse_mode="HTML")
                    break
                
                for user in users:
                    user_id = user['username']
        
                    try:
                        if len(comments_used) == len(comments):
                            raise Exception("All comments have been used!")

                        for random_comment in comments:
                            if random_comment not in comments_used:
                                comments_used.append(random_comment)
                                print(len(comments_used))
                                print(len(comments))
                        
                                await client.send_message(user_id, random_comment)
                                await send_message_to_user(user_id)
                                message_send +=1
                                
                                await asyncio.sleep(3)
                                break

                        if message_send >=15:
                            break
                        
                        if message_failed >=8:
                            await bot.send_message(cha_id=message.chat.id,
                                                   text="<b>Проблеми з надсиланням!</b>",
                                                   parse_mode="HTML")
                            break
                    except Exception as e:
                        print(f"Error sending message to user with user_id {user_id}: {e}")
                        message_failed +=1
                        problem_ids.append(user_id)
                
                
                await bot.send_message(chat_id=message.chat.id,
                            text=f"<b>👻 Успішно!\n\n✅ Надіслано: {message_send}\n❌ Не надіслано: {message_failed}\nПроблематичні ID: {problem_ids}</b>",
                            parse_mode="HTML")
                
                message_send = 0
                message_failed = 0
                problem_ids.clear()
            
            except PhoneNumberBannedError:
                print(f"Phone number is banned for {random_account['name']}")
                banned_accounts_count.add(random_account['session'])
                await bot.send_message(chat_id=message.chat.id,
                                        text=f"<b>🪓 Аккаунт {random_account['name']} забанено!</b>",
                                        parse_mode="HTML")
                await client.disconnect()
                continue
            
            except Exception as e:
                print(f"An error occurred: {e}")
                await bot.send_message(chat_id=message.chat.id,
                                        text=f"<b>Як залупа при надсиланні, сконтактуйтеся з адміністратором!</b>",
                                        parse_mode="HTML")
                await client.disconnect()
                break
            
            finally:
                await asyncio.sleep(1)
                await client.disconnect()
            
        break
        
    if len(accounts) == len(banned_accounts_count):
        await bot.send_message(chat_id=1013673667, #624076500
                           text="<b>🤯 Кекіч, всі аккаунти нахуй перебанили.</b>",
                           parse_mode="HTML")
            
            
@dp.message_handler(text='Вимкнути бота ❌')
async def shut_down_handler(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text="<b>🤨 Дійсно вимкнути?</b>",
                           reply_markup=bot_turnoff_keyboard(),
                           parse_mode="HTML")
    
@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('turnoff_'))
async def shut_down_proof(callback: types.CallbackQuery):
    details = callback.data.split('_')[1]
    
    if details == "accept":
        turn_off_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await bot.send_message(chat_id=callback.message.chat.id,
                               text='<b>👋 Бота вимкнено!</b>',
                               parse_mode="HTML")
        
        announcement_type = 'turn_off'
        await user_announcement(announcement_type, turn_off_time, None)
        sys.exit()
    
    if details == "cancel":
        await bot.edit_message_text(chat_id=callback.message.chat.id,
                                    message_id=callback.message.message_id,
                                    text='<b>❌ Відміна</b>',
                                    parse_mode="HTML")
        
@dp.message_handler(text='Аккаунти 💭')
async def banned_check_handler(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=1)

    if accounts:
        for account in accounts:
            try:
                account_identifier = await generate_credentials_indentifier(account['session'], account['phone_number'], account['name'])
                button_text = f"{account['name']}-{account['session']}"
                button_callback_data = f"accounts_{account_identifier}"
                
                message_mapping[account_identifier] = {
                    'session': account['session'],
                    'phone_number': account['phone_number'],
                    'name': account['name']
                }
                
                keyboard.add(InlineKeyboardButton(text=button_text, callback_data=button_callback_data))
            
            except KeyError:
                print(f"Error! Невідома помилка з аккаунтами!")
            
        
        response_message = "<b>Список аккаунтів 📄</b>"
    
    else:
        response_message = "<b>🙁 Список аккаунтів пустий</b>"
 
    
    await bot.send_message(chat_id=message.chat.id, 
                           text=response_message, 
                           parse_mode="HTML", 
                           reply_markup=keyboard)


async def database_check_handler(message: types.Message):
    try:
        posts = await database_check("all")

        if not posts:
            await bot.send_message(chat_id=message.chat.id,
                                   text="<b><🤨 База даних пуста!</b>",
                                   parse_mode="HTML")

        else:
            response = "<b>Всі користувачі:\nID | User ID | Дата | Статус</b>\n\n"
            for post in posts:
                user_info = f"<b>{post['id']} | {post['user_id']} | {post['date_added']} | {post['status']}</b>"
                response += user_info + "\n"

            # Split the response into chunks of 4000 characters
            message_chunks = [response[i:i + 4000] for i in range(0, len(response), 4000)]

            # Send each chunk as a separate message
            for chunk in message_chunks:
                await bot.send_message(chat_id=message.chat.id,
                                       text=chunk,
                                       parse_mode="HTML")

    except Exception as ex:
        await bot.send_message(chat_id=message.chat.id,
                               text="ERROR",
                               parse_mode="HTML")
        print("Unknown mistake, probably with Database!")


         
         
@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('accounts_'))
async def banned_check_callback(callback: types.CallbackQuery):
    account_identifier = callback.data.split('_')[1]
    account_details = message_mapping.get(account_identifier)
    
    if account_details:
        session = account_details['session']
        phone_number = account_details['phone_number']
        name = account_details['name']
        
    message_text = STRUCTURED_MESSAGE.format(name=name,
                                             session=session,
                                             phone_number=phone_number)
    
    await bot.send_message(chat_id=callback.message.chat.id,
                           text=message_text,
                           reply_markup=check_banned(session, phone_number),
                           parse_mode="HTML")   


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('ban_'))
async def banned_check_completely(callback: types.CallbackQuery):
    session = callback.data.split('_')[2]
    phone_number = callback.data.split('_')[-1]
    choice = callback.data.split('_')[1]

    async with client_lock:
        client = TelegramClient(session, "20600849", "41b4269e451bb95f0a2bfdd61d52947e", proxy=proxy)
        await client.connect()
        try:
            if not await client.is_user_authorized():
                await client.send_code_request(phone=phone_number)

            if choice == "completely":
                await bot.send_message(chat_id=callback.message.chat.id,
                                        text="<b>Аккаунт живий!</b>",
                                        parse_mode="HTML")
            elif choice == "spam":
                await client.send_message('@SpamBot', '/start')

                async for message in client.iter_messages('@SpamBot', limit=1):
                    await bot.send_message(chat_id=callback.message.chat.id,
                                           text=message.text,
                                           parse_mode="HTML")

        except PhoneNumberBannedError:
            await bot.send_message(chat_id=callback.message.chat.id,
                                    text="<b>Аккаунт забанено!</b>",
                                    parse_mode="HTML")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            await client.disconnect()





# @dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('ban_'))
# async def banned_check_completely(callback: types.CallbackQuery):
#     session = callback.data.split('_')[2]
#     phone_number = callback.data.split('_')[-1]
#     choice = callback.data.split('_')[1]

#     if choice == "completely":
#         async with client_lock:
#             client = TelegramClient(session, "20600849", "41b4269e451bb95f0a2bfdd61d52947e")
#             await client.connect()
#             if not await client.is_user_authorized():
#                 try:
#                     await client.send_code_request(phone=phone_number)
#                     await bot.send_message(chat_id=callback.message.chat.id,
#                             text="<b>Аккаунт живий!</b>",
#                             parse_mode="HTML")
#                 except PhoneNumberBannedError:
#                     await bot.send_message(chat_id=callback.message.chat.id,
#                                            text="<b>Аккаунт забанено!</b>",
#                                            parse_mode="HTML")
#                 except Exception as e:
#                     print(f"An error occurred: {e}")
#                 finally:
#                     await client.disconnect()
    
#     if choice == "spam":
#             client = TelegramClient(session, "20600849", "41b4269e451bb95f0a2bfdd61d52947e")
#             await client.connect()

#             try:
#                 await client.send_message('@SpamBot', '/start')
                
#                 async for message in client.iter_messages('@SpamBot', limit=1):
#                     await bot.send_message(chat_id=callback.message.chat.id,
#                                      text=message.text,
#                                      parse_mode="HTML")
                
#             except Exception as e:
#                 print(f"An error occurred: {e}")
#             finally:
#                 await client.disconnect()
    
            
if __name__ == "__main__":
    dp.middleware.setup(CheckSubscriptionUserMiddleware())
    executor.start_polling(dp, skip_updates=True)
