import telethon
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl import types
import asyncio
from python_socks import ProxyType
import time

api_id = "20600849"
api_hash = "41b4269e451bb95f0a2bfdd61d52947e"

#Україна 24/7 | Test_channel_3 | ТОПОР - Горячие новости | ТОПЛЕС | НЕ МОРГЕНШЕРН | CSGO | 4PDA Community | Канал для работников 5/2 | Новости Москвы | Труха Украина | мы вам перезвоним
group_ids = ['https://t.me/ukraina_novosti', 
             'https://t.me/deniszhhuta_testchannel_3', 
             'https://t.me/topor', 'https://t.me/toplesofficial', 
             'https://t.me/nemorgenshtern', 'https://t.me/csgo_main', 
             'https://t.me/pda4_forum', 'https://t.me/kdrabotnikov', 
             'https://t.me/moscowmap', 'https://t.me/truexanewsua', 
             'https://t.me/ca11_you']

#group_ids = [-1001288489154, -1001242446516, -1001237513492, -1001199360700, -1001214137365, -1001654574049, -1001003313758, -1001196199866, -1001967505770, -1001279115440, -1001592724979, -1001777186853, -1001851926963]

proxy = {
        'proxy_type': ProxyType.SOCKS5,
        'addr': "45.56.124.180",
        'port': 27614,
        'username': "modeler_2B6ifs",
        'password': "aNIxmx0U6huI",
        'rdns': True
        }

with TelegramClient('join_groups', api_id, api_hash) as client:
    client.start()
    client.connect()
    
    for group_id in group_ids:
        try:
            #entity = types.InputPeerChannel(group_id, 0)
            client(JoinChannelRequest(group_id))
            print(f"Joinder group/channel with ID: {group_id}")
            time.sleep(1)
        
        except Exception as e:
            print(f"Error joining group/channel with ID: {group_id}: {str(e)}")
            time.sleep(3)
            
    print("All requested groups/channels were joined!")