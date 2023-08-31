import telethon
from telethon import TelegramClient, events
from telethon.events import ChatAction
from telethon.tl.types import PeerChannel
from telethon import functions, types
import asyncio
import csv
import random
import threading
from addition import logs_handler, send_telegram_announcement
import os
from python_socks import ProxyType


chat_listen_to = []
comments = []
comments_used = []


bot_banned_chat = {}
client_lock = asyncio.Lock()


accounts = [
    {"api_id": "24607193", "api_hash": "75e0b0af6c73a423bb12bc1ee0e9c14c", "session": "session_01", "name": "Andrey_bot"}, #Andrey
    {"api_id": "23255984", "api_hash": "fca003b16ca72a7ca5ddb6762985e3c2", "session": "session_02", "name": "Angelo_bot"} #Max
]


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
        if row:  # Check if the row is not empty
            message_text = row[0]
            comments.append(message_text.strip())

       

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
            async with TelegramClient(random_account['session'], random_account['api_id'], random_account['api_hash'], proxy=proxy) as client:
                client.start()
                client.connect()
                
                # Check if the account is banned before sending a message
                if chat_id in bot_banned_chat:
                    banned_bot_names = {bot['name'] for bot in bot_banned_chat[chat_id]}
                    if banned_bot_names == {account['name'] for account in accounts}:
                        print(f"All bots are banned for chat {chat_id}. Stopping the loop.")
                        client.disconnect()
                        return  # Break the loop
                
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
                name_bot = [str(random_account["name"]).strip()]
                
                try:
                    print(chat_id, "HERE")
                    await client.send_message(PeerChannel(channel_id=chat_id), random_comment, comment_to=reply_to_message_id)
                    await logs_handler(filename, chat_id_converted, message_id_converted, name_bot)
                
                except telethon.errors.rpcerrorlist.ChannelPrivateError as e:
                    try:
                        print("Channel is private or bot is banned from the channel:", chat_entity.title, "with ID:", chat_id)
                        await send_telegram_announcement(chat_entity.title, chat_id, name_bot)
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
                delay_seconds = random.uniform(5, 10)
                await asyncio.sleep(delay_seconds)

                chat_entity = await client.get_entity(event.chat_id)
                await send_message_from_random_account(event.chat_id, random_comment, message_to_comment.id, chat_entity)
                break

            else:
                print("Comment is already used. Skipping...")
          
                                  
client.start()
client.run_until_disconnected()