import telethon
import asyncio
import logging
import random
import os
import csv
from telethon import TelegramClient, events
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.account import UpdateUsernameRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.errors.rpcerrorlist import PhoneNumberBannedError
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from configuration import *
from db import *

channel_id = -4000777712

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s]: %(message)s',
    handlers=[
        logging.FileHandler('spammer.log'),
        logging.StreamHandler()
    ]
)


group_ids = []
group_links = []
comments = []
comments_used = []

logger = logging.getLogger('spammer_02')


with open('/Users/zgutadenis/Desktop/Work/SpamBot2.0_Petrov/chats.csv', 'r') as file:
    csvreader = csv.reader(file, delimiter=',')
    for row in csvreader:
        if len(row) >= 2:
            group_link = row[0]
            group_id = row[1]
            group_links.append(group_link)
            group_ids.append(group_id)

# with open('/Users/zgutadenis/Desktop/Work/SpamBot_Petrov/messages.csv', 'r') as file:
#     csvreader = csv.reader(file, delimiter='/')
#     for row in csvreader:
#         if row:
#             message_text = row[0]
#             comments.append(message_text.strip())

async def join_groups_for_account(account):
    async with TelegramClient(account['session'], account['api_id'], account['api_hash']) as client_1:
        await client_1.connect()
        await client_1.start()
        
        random.shuffle(photos)
        random_photo = random.choice(photos)
        random_nickname = random.choice(telegram_nicknames)

        for group_link in group_links:
            try:
                await client_1(JoinChannelRequest(group_link))
                logger.info(f"Join group/channel with ID: {group_link} еfor {account['name']}")
                await asyncio.sleep(1)
            except Exception as e:
                logger.error(f"Error joining group/channel with ID: {group_link} for {account['name']}: {str(e)}")
                await asyncio.sleep(3)
        
        print(f"All requested groups/channels were joined for {account['name']}")
        
        await client_1(UpdateProfileRequest(
            about='Весь треш тут -> @trish_vids',
            first_name=random_nickname
        ))
        await asyncio.sleep(2)
        
        file = await client_1.upload_file(random_photo)
        await client_1(UploadProfilePhotoRequest(file=file))
        
        await asyncio.sleep(2)
        await client_1.disconnect()

async def join_chats():
    for account in accounts:
        await join_groups_for_account(account)


#Головний бот, що перевіряє повідомлення
client = TelegramClient("main_bot", API_ID, API_HASH)

@client.on(events.NewMessage(chats=channel_id))
async def new_message_handler(event):
    if event.message:
        user_id = event.sender_id
        await add_id(user_id)



if __name__ == "__main__":
    #loop = asyncio.get_event_loop()
    #loop.run_until_complete(join_chats())
    
    client.start()
    client.run_until_disconnected()