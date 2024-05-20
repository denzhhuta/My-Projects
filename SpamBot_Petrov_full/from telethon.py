from telethon.sync import TelegramClient, events
from telethon.tl import types

# Your API credentials
api_id = '20600849'
api_hash = '41b4269e451bb95f0a2bfdd61d52947e'


# Initialize the Telegram client
client = TelegramClient('main_bot', api_id, api_hash)

@client.on(events.NewMessage(chats=-1001626553821))
async def handle_new_message(event):
    # Get the sender's user information
    sender = await event.get_sender()
    
    if sender.username:
        print(f"Message from @{sender.username}")
    else:
        print(f"Message from {sender.first_name} {sender.last_name}: {event.text}")

async def main():
    # Start the Telethon client
    await client.start()
    
    # Run the client until it's stopped manually
    await client.run_until_disconnected()

if __name__ == "__main__":
    client.loop.run_until_complete(main())





