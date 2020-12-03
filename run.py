import re, os, sys, csv, json, datetime, logging
from re import findall
from sqlite3 import Error
from telethon import TelegramClient, events, utils, functions, sync, Button, connection, helpers, types
from telethon.hints import Entity
from telethon.tl.types import PeerChannel
from telethon.utils import get_input_peer

#LOGGING FORMATE AND DETIALS
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)

bot = TelegramClient('MON_PO_DOG', API_ID, API_HASH)#.start(bot_token=BOT_TOKEN)

@bot.on(events.NewMessage)
async def mon(msg):
    ###SENDER INFO
    senderinfo = await msg.get_sender() #提取所有陬訊人資訊
    sender_entity = await bot.get_entity(senderinfo) # = senderinfo
    sender_peer = await bot.get_input_entity(senderinfo) #發訊人USER_ID + ACCESS_HASH(完整資訊)
    PeerID = utils.get_peer(sender_peer) #提取 sender_peer 內的 Peer(完整資訊) 範例：PeerUser(user_id=1376181547)
    Peer_UserID = utils.get_peer_id(sender_peer) #提取 sender_peer 內的 User ID(獨立的User ID)
    Peer_UserHASH = sender_peer.access_hash #提取從 Peer_User 中的 access_hash
    InPut_User = utils.get_input_user(senderinfo) #提取發訊人所有資料
    sender_id = InPut_User.user_id #從發訊人資料中提取 USER ID
    sender_dp_name = utils.get_display_name(senderinfo) #提取發訊人完整顯示名稱
    if senderinfo.username is None: #提取並檢測發訊人使用者名稱，如果沒有設定即‘未設定’，如果有即加入@ 範例：@Anonymous
        sender_uid = '未設定'
    else:
        sender_uid = '@' + senderinfo.username
    if sender_entity.phone is None: #提取並檢測發訊人電話號碼，如果沒有設定即‘未設定’，（警告！使用者必要設定公開，否即不會顯示）
        sender_phone = '未設定'
    else:
        sender_phone = sender_entity.phone

    ###MSG INFO
    msginfo = msg.message #提取訊息內容
    msg_entity = await bot.get_messages(senderinfo) #以 utils API讀取完整訊息
    msg_input = utils.get_input_message(msginfo) #完整的Message ID資
    msg_id = utils.get_message_id(msginfo) #獨立的Message ID資訊
    PeerChecker = msginfo.peer_id #檢測訊息的去向在Channel或Chat

    ###CHECKER
    Peer_U = re.compile('PeerUser')
    Peer_CH = re.compile('PeerChannel')

    if Peer_CH.findall(str(PeerChecker)):
        CH_ID = PeerChecker.channel_id
        CH_INFO = await bot.get_entity(PeerChannel(CH_ID))
        CH_TITLE = CH_INFO.title

        print('--------------CH DEBUG--------------')
        print('CHANNEL TITLE: ' + str(CH_TITLE))
        print('CHANNEL ID: ' + str(CH_ID))
        print('------------SENDER DEBUG------------')
        #print(sender_entity.stringify())
        #print('SENDER INFO PEER: ' + str(sender_peer))
        print('Peer ID: ' + str(PeerID))
        print('Sender Peer: ' + str(sender_peer))
        print('User ACCESS_HASH: ' + str(Peer_UserHASH))
        print('USER ID: ' + str(sender_id))
        print('USER DISPLAY NAME: ' + str(sender_dp_name))
        print('USER USER ID: ' + str(sender_uid))
        print('USER PHONE NO: ' + str(sender_phone))
        print('------------------------------------')
        print('-------------MSG  DEBUG-------------')
        print('MSG ID: ' + str(msg_id))
        print('MSG INPUT: ' + str(msg_input))
        print('CONTENT:\n' + str(msginfo.text))

    elif Peer_U.findall(str(PeerChecker)):
        print('-------------CHAT DEBUG-------------')
        #print('CHANNEL INFO: ' + str(DEBUG))
        print('------------SENDER DEBUG------------')
        #print(sender_entity.stringify())
        #print('SENDER INFO PEER: ' + str(sender_peer))
        #print('Peer ID: ' + str(PeerID))
        print('Sender Peer: ' + str(sender_peer))
        print('User ACCESS_HASH: ' + str(Peer_UserHASH))
        print('USER ID: ' + str(sender_id))
        print('USER DISPLAY NAME: ' + str(sender_dp_name))
        print('USER USER ID: ' + str(sender_uid))
        print('USER PHONE NO: ' + str(sender_phone))
        print('------------------------------------')
        print('-------------MSG  DEBUG-------------')
        print('MSG ID: ' + str(msg_id))
        print('MSG INPUT: ' + str(msg_input))
        print('CONTENT:\n' + str(msginfo.text))
        #print(msginfo.stringify())
        #print(msg_entity)    

bot.start()
with bot:
    bot.run_until_disconnected()
