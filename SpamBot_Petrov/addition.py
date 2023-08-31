import csv
import os
import asyncio
import aiogram
from datetime import datetime
from aiogram import types, Bot, Dispatcher, executor

bot = aiogram.Bot("6064195503:AAHdQeQ6LA4T2BPoDTBozkOucEIwCTcliQo")

async def send_telegram_announcement(channel_name, channel_id, name_bot):
    action_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    announcement_message = f"<b>Можливо бота {name_bot} забанили в {channel_name} з ID: {channel_id}</b>"
    await bot.send_message(chat_id=1013673667,
                           text=announcement_message,
                           parse_mode="HTML")

async def logs_handler(filename, chat_id, message_id, name_bot):
    try:
        with open(filename, 'a+', newline='') as file:
            if file.tell() == 0: # чи пустий
                writer = csv.writer(file)
                writer.writerow(['Chat_ID', 'Message_ID', 'Time', 'Name_Bot'])
            file.seek(0, os.SEEK_END)
            writer = csv.writer(file)
            action_time = [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
            writer.writerows(zip(chat_id, message_id, action_time, name_bot))
            
        print("Succesfully appended")
    
    except Exception as e:
        print(f"Error appending emails and IBANs to CSV file: {filename}\n{e}")
            

