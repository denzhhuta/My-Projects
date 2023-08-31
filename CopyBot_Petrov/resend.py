from telethon import TelegramClient, events
import asyncio
import csv
from configuration import CONFIGURATION
import os

chats_to_listen_to = []

with open('/Users/zgutadenis/Desktop/Work/CopyBot_Petrov/chats.csv', 'r') as file:
    csvreader = csv.reader(file, delimiter=',')
    for row in csvreader:
    #['ID_GROUP', '-23124513512']
        if len(row) == 2:
            chat_name, chat_id = row
            chat_id = chat_id.strip().replace('\\', '')
            if chat_id.startswith('-'):
                chats_to_listen_to.append(int(chat_id))

client = TelegramClient('session0', CONFIGURATION['API_ID'], CONFIGURATION['API_HASH'])


@client.on(events.NewMessage(chats=chats_to_listen_to))
async def new_message_handler(event):
    if event.sender_id == CONFIGURATION['ID_BOT']:
        return
    
    if event.grouped_id:
        return
    
    # and event.message.text
    if event.message.video:
        print(event)
        await client.forward_messages(entity=CONFIGURATION['ID_BOT'], messages=event.message)


client.start()
client.run_until_disconnected()
