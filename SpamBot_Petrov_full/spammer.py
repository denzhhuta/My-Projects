import telethon
from telethon import TelegramClient, events
from telethon.events import ChatAction
from telethon.tl.types import PeerChannel
from telethon.tl import types
from addition import logs_handler, send_telegram_announcement
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.errors.rpcerrorlist import PhoneNumberBannedError
from telethon.tl.functions.photos import UploadProfilePhotoRequest
from configuration import *
import asyncio
import csv
import random
import threading
import os
import time
import logging
import random
import re
import sys
import os
import glob
import itertools


chat_listen_to = []
chat_joined_to = []
bot_banned_chat = {}
client_lock = asyncio.Lock()
last_response_time = {}
accounts = []
current_directory = os.getcwd()
session_folder = current_directory


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s]: %(message)s',
    handlers=[
        logging.FileHandler('spammer.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('spammer')


def process_template(template):
    def replace(match):
        options = match.group(1).split('|')
        return random.choice(options)

    while "{" in template:
        template = re.sub(r'{([^{}]+)}', replace, template)

    return template


def iterate_sessions():
    phone_number_pattern = re.compile(r'^\d+$')
    #glob.glob - шукає файли що задовільняють паттер і відсилає повний шлях, os.path.join - це вже робить сам патерн, шукаючи файли в папці
    for session_file in glob.glob(os.path.join(session_folder, '*.session')):
        #os.path.basename - бере тільки назву файлу, без повного його шляхy, os.path.splitext - розділяє назву файлу від розширення в форматі ['name' '.session'], тому [0]
        session_name = os.path.splitext(os.path.basename(session_file))[0]
        
        if phone_number_pattern.match(session_name) and session_name != 'main_bot':
                
                account_info = {
                    "api_id": "20600849",
                    "api_hash": "41b4269e451bb95f0a2bfdd61d52947e",
                    "session": session_name,
                    "phone_number": session_name,
                    "name": session_name
                }              
                
                accounts.append(account_info)
                
        else:
            if session_name != 'main_bot':
                print(f"Неправильно названий файл {session_name}, що знаходиться {session_file}")
        

with open('/Users/zgutadenis/Desktop/Work/SpamBot_Petrov/chats.csv', 'r') as file:
    csvreader = csv.reader(file, delimiter=',')
    for row in csvreader:
        if len(row) == 2:
            chat_name, chat_id = row
            if chat_id.startswith('-'):
                if chat_name != "https://t.me/trish_vids":
                    chat_listen_to.append(int(chat_id))
                chat_joined_to.append(chat_name)


#grouped_accounts = [accounts[i:i+4] for i in range(0, len(accounts), 4)]
def associate_proxies(accounts, proxies):
    grouped_accounts = []
    #тут воно з кроком 4, щоб робити групи по 4
    for i in range(0, len(accounts), 4):
        group = accounts[i:i+4]
        grouped_accounts.append(group)
    
    #itertools.cycly - безкінечний луп, що завжди повторюється по всіх проксі [1,2,3] - завжди 123123
    for group, proxy in zip(grouped_accounts, itertools.cycle(proxies)):
        for account in group:
            account['proxy'] = proxy
                 

async def join_groups_for_account(account):
        client_1 = TelegramClient(account['session'], account['api_id'], account['api_hash'])
        await client_1.connect()  
                
        if not await client_1.is_user_authorized():
                try:
                    await client_1.send_code_request(phone=account['phone_number'])
                except PhoneNumberBannedError:
                    name_bot = [str(account["name"]).strip()]
                    print(f"Phone number is banned for {account['name']}")
                    return
                    
        random.shuffle(photos)
        random_photo = random.choice(photos)
        random_nickname = random.choice(telegram_nicknames)
        
        for group_id in chat_joined_to:
            try:
                await client_1(JoinChannelRequest(group_id))
                logger.info(f"Join group/channel with ID: {group_id} for {account['name']}")
                await asyncio.sleep(2)
            except Exception as e:
                 logger.error(f"Error joining group/channel with ID: {group_id} for {account['name']}: {str(e)}")
                 await asyncio.sleep(2)
                        
        print(f"All requested groups/channels were joined for {account['name']}")
        
        await client_1(UpdateProfileRequest(
            about='Весь треш тут -> @trish_vids',
            first_name=random_nickname
        ))
        await asyncio.sleep(2)
        
        file = await client_1.upload_file(random_photo)
        await client_1(UploadProfilePhotoRequest(file=file))
        
        await asyncio.sleep(1)
        await client_1.disconnect()
    
async def join_chats():
    for account in accounts:
        await join_groups_for_account(account)


client = TelegramClient("main_bot", API_ID, API_HASH)

async def send_message_from_random_account(chat_id, random_comment, reply_to_message_id, chat_entity):
    banned_accounts_count = set()
    while banned_accounts_count < len(accounts):
        random_account = random.choice(accounts)
        
        async with client_lock:
            client = TelegramClient(random_account['session'], random_account['api_id'], random_account['api_hash'])
            await client.connect()
            if not await client.is_user_authorized():
                try:
                    await client.send_code_request(phone=random_account['phone_number'])
                except PhoneNumberBannedError:
                    name_bot = [str(random_account["name"]).strip()]
                    print(f"Phone number is banned for {random_account['name']}")
                    await send_telegram_announcement(random_account['session'], 999, random_account['name'], 3)
                    await client.disconnect()
                    banned_accounts_count.add(random_account['session'])
                    accounts.remove(random_account)
                    continue
                        
            name_bot = [str(random_account["name"]).strip()]
            
            # Check if the account is banned before sending a message
            if chat_id in bot_banned_chat:

                banned_bot_names = {bot['name'] for bot in bot_banned_chat[chat_id]}
                if banned_bot_names == {account['name'] for account in accounts}:
                    await send_telegram_announcement(chat_entity.title, chat_id, name_bot, 2)
                    print(f"All bots are banned for chat {chat_id}. Stopping the loop.")
                    await client.disconnect()
                    return
            
                if any(bot['name'] == random_account['name'] for bot in bot_banned_chat[chat_id]):
                    print(f"Bot '{random_account['name']}' is banned for chat {chat_id}")
                    await client.disconnect()
                    continue
            
            print("Sending message from account:", random_account)
            print("Chat ID:", chat_id)
            print("Random Comment:", random_comment)
            print("Reply to Message ID:", reply_to_message_id)
            
            chat_id_converted = [str(chat_id).strip()]
            message_id_converted = [str(reply_to_message_id).strip()]
            filename = os.path.join("/Users/zgutadenis/Desktop/Work/SpamBot_Petrov", "logs.csv")
            
            try:
                print(chat_id, "HERE")
                await client.send_message(PeerChannel(channel_id=chat_id), random_comment, comment_to=reply_to_message_id)
                await logs_handler(filename, chat_id_converted, message_id_converted, name_bot)
            
            except telethon.errors.rpcerrorlist.ChannelPrivateError as e:
                try:
                    print("Channel is private or bot is banned from the channel:", chat_entity.title, "with ID:", chat_id)
                    await send_telegram_announcement(chat_entity.title, chat_id, name_bot, 1)
                    
                    new_banned_entry = {
                        'api_id': random_account['api_id'],
                        'api_hash': random_account['api_hash'],
                        'session': random_account['session'],
                        'name': random_account['name']
                    }
                    
                    if any(bot['name'] == new_banned_entry['name'] for bot in bot_banned_chat.get(chat_id, [])):
                        print(f"Bot '{new_banned_entry['name']}' already exists for chat {chat_id}")
                    else:
                        bot_banned_chat.setdefault(chat_id, []).append(new_banned_entry)
                        print(f"Added bot '{new_banned_entry['name']}' to chat {chat_id}")

                
                except telethon.errors.rpcerrorlist.ChannelPrivateError:
                    print("Channel ID:", chat_id , "is inaccessible due to privacy. Maybe you were banned!")
                    break
            
            except telethon.errors.rpcerrorlist.ChatWriteForbiddenError:
                print("Bot doesn't have permission to send messages to this chat.")
                break
                    
            except ValueError as ve:
                print("Error: ", ve)
                print("Handling the ValueError for input entity not found.")
                
                new_banned_entry = {
                    'api_id': random_account['api_id'],
                    'api_hash': random_account['api_hash'],
                    'session': random_account['session'],
                    'name': random_account['name']
                }
                
                if any(bot['name'] == new_banned_entry['name'] for bot in bot_banned_chat.get(chat_id, [])):
                    print(f"Bot '{new_banned_entry['name']}' already exists for chat {chat_id}")
                else:
                    bot_banned_chat.setdefault(chat_id, []).append(new_banned_entry)
                    print(f"Added bot '{new_banned_entry['name']}' to chat {chat_id}")
            
            finally:
                await client.disconnect()
                await asyncio.sleep(30)
                break
    
    if len(accounts) == len(banned_accounts_count):
        await send_telegram_announcement(1,1,1,4)


@client.on(events.NewMessage(chats=chat_listen_to))
async def new_message_handler(event):
    message_to_comment = event.message
    chat_name = event.chat.title if event.chat.title else "Unknown"    
    print(f"Received message in group '{chat_name}': {message_to_comment.text}")

    if message_to_comment.chat_id and message_to_comment.replies is not None:
        random_comment = process_template(text)
        last_response = last_response_time.get(event.chat_id)
        if last_response is not None:
            time_since_last_response = asyncio.get_event_loop().time() - last_response
            if time_since_last_response < 30:
                delay_seconds = random.uniform(5, 10)
            else:
                delay_seconds = random.uniform(8, 15)
        else:
            delay_seconds = random.uniform(5, 10)

        await asyncio.sleep(delay_seconds)

        chat_entity = await client.get_entity(event.chat_id)
        await send_message_from_random_account(event.chat_id, random_comment, message_to_comment.id, chat_entity)
        last_response_time[event.chat_id] = asyncio.get_event_loop().time()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    iterate_sessions() 
    print(accounts)
    
    while True:
        joint_chats_check = input("Чи потрібно встувати в групи? (yes/no): ").strip().lower()
        
        if joint_chats_check == "yes":
            print("Окей, вступаємо в групи!")        
            loop.run_until_complete(join_chats())
            break
        
        elif joint_chats_check == "no":
            print("Окей, не вступаємо в групи!")
            break
        
        else:
            print("Кекіч, ти єблан? Написано yes/no")
            sys.exit(1)
        
         
    client.start()
    client.run_until_disconnected()