import telethon
from telethon import TelegramClient, events
from telethon.events import ChatAction
from telethon.tl.types import PeerChannel
from telethon.tl import types
from addition import logs_handler, send_telegram_announcement
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.errors.rpcerrorlist import PhoneNumberBannedError
from python_socks import ProxyType
import asyncio
import csv
import random
import threading
import os
import time
import logging

chat_listen_to = []
comments = []
comments_used = []
bot_banned_chat = {}
client_lock = asyncio.Lock()
last_response_time = {}


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s]: %(message)s',
    handlers=[
        logging.FileHandler('spammer.log'),
        logging.StreamHandler()
    ]
)

# Create a logger instance
logger = logging.getLogger('spammer')


accounts = [
    {"api_id": "", "api_hash": "", "session": "join_groups_1", "phone_number": "", "name": "Andrey_bot"}#Andrey
    #{"api_id": "23255984", "api_hash": "fca003b16ca72a7ca5ddb6762985e3c2", "session": "session_02", "name": "Angelo_bot"} #Max
]

group_ids = ['https://t.me/ukraina_novosti', 
             'https://t.me/deniszhhuta_testchannel_3', 
             'https://t.me/topor', 'https://t.me/toplesofficial', 
             'https://t.me/nemorgenshtern', 'https://t.me/csgo_main', 
             'https://t.me/pda4_forum', 'https://t.me/kdrabotnikov', 
             'https://t.me/moscowmap', 'https://t.me/truexanewsua', 
             'https://t.me/ca11_you']


with open('/Users/zgutadenis/Desktop/Work/CopyBot_Petrov/chats.csv', 'r') as file:
    csvreader = csv.reader(file, delimiter=',')
    for row in csvreader:
        if len(row) == 2:
            chat_name, chat_id = row
            chat_id = chat_id.strip().replace('\\', '')
            if chat_id.startswith('-'):
                chat_listen_to.append(int(chat_id))

print(chat_listen_to)
with open('/Users/zgutadenis/Desktop/Work/SpamBot_Petrov/messages.csv', 'r') as file:
    csvreader = csv.reader(file, delimiter='/')
    for row in csvreader:
        if row:
            message_text = row[0]
            comments.append(message_text.strip())

async def join_groups_for_account(account):
    proxy = {
        'proxy_type': ProxyType.SOCKS5,
        'addr': "45.56.124.180",
        'port': 27614,
        'username': "modeler_2B6ifs",
        'password': "aNIxmx0U6huI",
        'rdns': True
        }
    async with TelegramClient(account['session'], account['api_id'], account['api_hash']) as client_1:
        await client_1.start()
        await client_1.connect()   
        for group_id in group_ids:
            try:
                await client_1(JoinChannelRequest(group_id))
                logger.info(f"Join group/channel with ID: {group_id} for {account['name']}")
                await asyncio.sleep(4)
            except Exception as e:
                 logger.error(f"Error joining group/channel with ID: {group_id} for {account['name']}: {str(e)}")
                 await asyncio.sleep(3)
                        
        print(f"All requested groups/channels were joined for {account['name']}")
        await client_1(UpdateProfileRequest(
            about='@trish_vids'
        ))
        await asyncio.sleep(2)
        await client_1.disconnect()
    
async def join_chats():
    for account in accounts:
        await join_groups_for_account(account)

API_ID = "20600849"
API_HASH = '41b4269e451bb95f0a2bfdd61d52947e'

client = TelegramClient("main_bot", API_ID, API_HASH)

async def send_message_from_random_account(chat_id, random_comment, reply_to_message_id, chat_entity):
    while True:
        random_account = random.choice(accounts)
        
        async with client_lock:
            proxy = {
                'proxy_type': ProxyType.SOCKS5,
                'addr': "45.56.124.180",
                'port': 27614,
                'username': "modeler_2B6ifs",
                'password': "aNIxmx0U6huI",
                'rdns': True
            }
            async with TelegramClient(random_account['session'], random_account['api_id'], random_account['api_hash']) as client:
                client.start()
                client.connect()
                
                name_bot = [str(random_account["name"]).strip()]
                
                # Check if the account is banned before sending a message
                if chat_id in bot_banned_chat:
                    banned_bot_names = {bot['name'] for bot in bot_banned_chat[chat_id]}
                    if banned_bot_names == {account['name'] for account in accounts}:
                        await send_telegram_announcement(chat_entity.title, chat_id, name_bot, 2)
                        print(f"All bots are banned for chat {chat_id}. Stopping the loop.")
                        client.disconnect()
                        return
                
                    if any(bot['name'] == random_account['name'] for bot in bot_banned_chat[chat_id]):
                        print(f"Bot '{random_account['name']}' is banned for chat {chat_id}")
                        client.disconnect()
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
                        comments_used.remove(random_comment)
                        
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
                    comments_used.remove(random_comment)
                    
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
                    client.disconnect()
                    await asyncio.sleep(30)
                    break


@client.on(events.NewMessage(chats=chat_listen_to))
async def new_message_handler(event):
    message_to_comment = event.message
    print("Received message:", message_to_comment.text)

    if message_to_comment.chat_id and message_to_comment.replies is not None:
        if len(comments_used) == len(comments):
            raise Exception("All comments have been used!")

        for random_comment in comments:
            if random_comment not in comments_used:
                comments_used.append(random_comment)
                print(len(comments_used))
                print(len(comments))

                # Calculate the delay based on the last response time or use a default delay
                last_response = last_response_time.get(event.chat_id)
                if last_response is not None:
                    time_since_last_response = asyncio.get_event_loop().time() - last_response
                    if time_since_last_response < 30:
                        delay_seconds = random.uniform(30, 50)
                    else:
                        delay_seconds = random.uniform(30, 50)
                else:
                    delay_seconds = random.uniform(30, 50)

                await asyncio.sleep(delay_seconds)

                chat_entity = await client.get_entity(event.chat_id)
                await send_message_from_random_account(event.chat_id, random_comment, message_to_comment.id, chat_entity)
                last_response_time[event.chat_id] = asyncio.get_event_loop().time()  # Update last response time

                break

            else:
                print("Comment is already used. Skipping...")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(join_chats())


    client.start()
    client.run_until_disconnected()

# @client.on(events.NewMessage(chats=chat_listen_to))
# async def new_message_handler(event):
#     message_to_comment = event.message
#     print("Received message:", message_to_comment.text)

#     if message_to_comment.chat_id and message_to_comment.replies is not None:
#         if len(comments_used) == len(comments):
#             raise Exception("All comments have been used!")

#         for random_comment in comments:
#             if random_comment not in comments_used:
#                 comments_used.append(random_comment)
#                 print(len(comments_used))
#                 print(len(comments))
#                 delay_seconds = random.uniform(30, 50)
#                 await asyncio.sleep(delay_seconds)

#                 chat_entity = await client.get_entity(event.chat_id)
#                 await send_message_from_random_account(event.chat_id, random_comment, message_to_comment.id, chat_entity)
#                 #await asyncio.sleep(30)
#                 break

#             else:
#                 print("Comment is already used. Skipping...")
