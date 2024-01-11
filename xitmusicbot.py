from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

import asyncio
import sqlite3
import datetime
from time import sleep

import config
import reply_markups
import inline_markups


db = sqlite3.connect('XIT MUSIC DATABASE.db', check_same_thread = False)
sql = db.cursor()

storage = MemoryStorage()
date_time = datetime.datetime.now().date()

bot = Bot(config.token)
dp = Dispatcher(bot, storage = MemoryStorage())

sql.execute('CREATE TABLE IF NOT EXISTS user_data (id INTEGER, username TEXT, firstname TEXT, lastname TEXT)')
db.commit()

class SearchState(StatesGroup):
    search = State()









#  CHECK SUBSCRIPTIONS

async def check_subscribtions(channels, user_id):
    for channel in channels:
        chat_member = await bot.get_chat_member(chat_id = channel[1], user_id = user_id)
        if chat_member['status'] == 'left':
            return False
    return True



#  START COMMAND

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):

    sql.execute(f'SELECT id FROM user_data WHERE id = ?', (message.chat.id,))
    user_id = sql.fetchone()

    if user_id is None:
        if await check_subscribtions(config.CHANNELS, message.from_user.id):
            await bot.send_message(message.chat.id, '<b> Добро пожаловать 👋 </b>', parse_mode='html', reply_markup = reply_markups.menu_reply)
            await insert_db(message)
        else:
            await bot.send_message(message.chat.id, '<b> Чтобы пользоваться ботом, подпишитесь на наши каналы ❗️ </b>', parse_mode = 'html', reply_markup = inline_markups.subscribe_inline)
    else:
        if await check_subscribtions(config.CHANNELS, message.from_user.id):
            await bot.send_message(message.chat.id, '<b> Добро пожаловать 👋 </b>', parse_mode='html', reply_markup = reply_markups.menu_reply)
        else:
            await bot.send_message(message.chat.id, '<b> Чтобы пользоваться ботом, подпишитесь на наши каналы ❗️ </b>', parse_mode = 'html', reply_markup = inline_markups.subscribe_inline)



#  INSERT DATA

async def insert_db(message):
    sql.execute('INSERT INTO user_data (id, username, firstname, lastname) VALUES (?, ?, ?, ?)',
    (message.chat.id, message.from_user.username, message.from_user.first_name, message.from_user.last_name))
    db.commit()



#  FORWARD

@dp.message_handler(commands = ['forward'])
async def forward(message):
    if message.chat.id == 5069231788:
        total = 0

        sql.execute('SELECT * FROM user_data')
        data = sql.fetchall()

        sql.execute('SELECT COUNT(id) FROM user_data')
        all_users = sql.fetchone()[0]

        for row in data:
            try:
                await bot.send_message(row[0], '<a href = "http://t.me/hittt_music?boost">⚠️ У тебя есть Telegram Premium? 😻</a>', parse_mode = 'html', reply_markup = inline_markups.link_inline)

                total += 1
                print(f'[{row[0]}]: получил сообщение  ✅')

            except:

                print(f'[{row[0]}]: заблокировал бота  ❌')

        else:
            blocked_users = all_users - total
            await bot.send_message(message.chat.id, f'<b>Количество пользователей:</b>  {all_users}', parse_mode = 'html', reply_markup = None)
            await bot.send_message(message.chat.id, f'<b>✅  Успешно получили:</b> {total}', parse_mode = 'html', reply_markup = None)
            await bot.send_message(message.chat.id, f'<b>❌  Заблокировавшие:</b> {blocked_users}', parse_mode = 'html', reply_markup = None)






#  USERS COUNT

@dp.message_handler(commands = ['users_count'])
async def users_count(message):

    sql.execute('SELECT COUNT(id) FROM user_data')
    all_users = sql.fetchone()[0]

    await bot.send_message(message.chat.id, f'Количество пользователей:  <b>{all_users}</b>', parse_mode = 'html')

#  ADMIN

@dp.message_handler(commands = ['admin'])
async def admin(message):
    if message.chat.id == 1020303972 or message.chat.id == 5069231788:
        await bot.send_message(message.chat.id, '<b> Выберите действие: </b>', parse_mode = 'html', reply_markup = reply_markups.admin_reply)
    else:
        await bot.send_message(message.chat.id, '<b> У вас нет прав на эту команду ❗️ </b>', parse_mode = 'html')





#  TEXT

@dp.message_handler(content_types = ['text'])
async def text(message):
    if await check_subscribtions(config.CHANNELS, message.from_user.id):

    #  NEW TRACKS

        if message.text == '🎙 Новинки' or message.text == 'Новинки':
            await bot.send_message(message.chat.id, '<b> Топ 10 новинок этой недели: </b>', parse_mode = 'html', reply_markup = inline_markups.week_17)
            await delete_message_1(message)

    #  REMIXES

        elif message.text == '🔥 Ремиксы' or message.text == 'Ремиксы':
            await bot.send_message(message.chat.id, '<b> Выберите язык: </b>', parse_mode = 'html', reply_markup = reply_markups.remix_language_reply)
            await delete_message_2(message)

    #  REMIX LANGUAGE

        elif message.text == '🇷🇺  Русские':
            await bot.send_message(message.chat.id, '<b> Выберите артиста: </b>', parse_mode = 'html', reply_markup = reply_markups.first_russian_artists_reply)
            await delete_message_2(message)

        elif message.text == '🇺🇸  Английские':
            await bot.send_message(message.chat.id, '<b> Выберите артиста: </b>', parse_mode = 'html', reply_markup = reply_markups.english_artists_reply)
            await delete_message_2(message)

    #  PAGES

        elif message.text == 'Следующая страница  ➡':
            await bot.send_message(message.chat.id, '<b> Выберите артиста: </b>', parse_mode = 'html', reply_markup = reply_markups.second_russian_artists_reply)
            await delete_message_1(message)

        elif message.text == '⬅  Предыдущая страница':
            await bot.send_message(message.chat.id, '<b> Выберите артиста: </b>', parse_mode = 'html', reply_markup = reply_markups.first_russian_artists_reply)
            await delete_message_1(message)

    #  SEARCH

        elif message.text == '🔍':
            await bot.send_message(
                chat_id = message.chat.id,
                text =
                '<b> Поиск по исполнителю  🔍</b>'
                '\nНапишите имя артиста, чтобы начать поиск.'
                '\n\nНапример:  <b>Miyagi</b>',
                parse_mode = 'html', reply_markup = reply_markups.cancel_reply)
            await SearchState.search.set()

    #  CHAT

        elif message.text == '📝  Чат' or message.text == 'Чат':
            await bot.send_message(message.chat.id, '<b> Чат канала для обсуждений 👇 </b>', parse_mode = 'html', reply_markup = inline_markups.chat_inline)
            await delete_message_1(message)

    #  PLAYLIST

        elif message.text == '📂  Плейлист':
            await bot.send_message(message.chat.id,'<b> В разработке... </b>', parse_mode = 'html', reply_markup = reply_markups.menu_reply)
            await delete_message_2(message)



    #  MAIN MENU

        elif message.text == '🏠  Главное меню':
            await bot.send_message(message.chat.id, '<b> Главное меню: </b>', parse_mode = 'html', reply_markup = reply_markups.menu_reply)
            await delete_message_1(message)

    #  BACK

        elif message.text == '⬅  Назад':
            await bot.send_message(message.chat.id,'<b> Выберите язык: </b>', parse_mode = 'html', reply_markup = reply_markups.menu_reply)
            await delete_message_1(message)

        elif message.text == '⬅   Назад':
            await bot.send_message(message.chat.id, '<b> Выберите язык: </b>', parse_mode = 'html', reply_markup = reply_markups.remix_language_reply)
            await delete_message_1(message)



    #  FORWARD TEXT

        elif message.text == 'Рассылка текста':
            if message.chat.id == 1020303972 or message.chat.id == 5069231788:
                await bot.send_message(message.chat.id,'<b> Введите текст: </b>', parse_mode = 'html', reply_markup = reply_markups.cancel_button)
            else:
                await bot.send_message(message.chat.id, '<b> У вас нет прав на рассылку ! </b>', parse_mode = 'html')

    #  FORWARD MUSIC

        elif message.text == 'Рассылка трека':
            if message.chat.id == 1020303972 or message.chat.id == 5069231788:
                await bot.send_message(message.chat.id, '<b> Отправьте трек: </b>', parse_mode = 'html', reply_markup = reply_markups.cancel_button)
            else:
                await bot.send_message(message.chat.id, '<b> У вас нет прав на рассылку ! </b>', parse_mode = 'html')















#  ENGLISH REMIXES

    #  BLACKBEAR

        elif message.text == 'BLACKBEAR':
            with open('Remix/English/BLACKBEAR/blackbear - idfc [aibek berkimbaev & shahrix remix].mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  CASSETTE

        elif message.text == 'CASSETTE':
            with open('Remix/English/CASSETTE/My Way (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  DAFT PUNK

        elif message.text == 'DAFT PUNK':
            with open('Remix/English/DAFT PUNK/Get Lucky (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  DUA LIPA

        elif message.text == 'DUA LIPA':
            with open('Remix/English/DUA LIPA/No Lie (ShaHriX & Camron Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  FOUSHEE

        elif message.text == 'FOUSHEE':
            with open('Remix/English/FOUSHEE/Deep End (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  G-EASY

        elif message.text == 'G-EASY':
            with open('Remix/English/G-EASY/Him & I (ShaHriX & Melix Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  GHOSTLY KISSES

        elif message.text == 'GHOSTLY KISSES':
            with open('Remix/English/GHOSTLY KISSES/Ghostly_Kisses_Empty_Note_Aibek_Berkimbaev_&_ShaHriX_remix.mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  IAN STORM

        elif message.text == 'IAN STORM':
            with open('Remix/English/IAN STORM/Run Away (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  INNA

        elif message.text == 'INNA':
            with open('Remix/English/INNA/Lonely (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/English/INNA/Solo (ShaHriX Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  JVLA

        elif message.text == 'JVLA':
            with open('Remix/English/JVLA/Such A Whole Remix.mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  KINA

        elif message.text == 'KINA':
            with open('Remix/English/KINA/Kina - Get You The Moon (ShaHriX & Amalee Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  LADY GAGA

        elif message.text == 'LADY GAGA':
            with open('Remix/English/LADY GAGA/Bloody Mary (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  LISA

        elif message.text == 'LISA':
            with open('Remix/English/LISA/Money (ShaHriX & TheBlvcks  Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  MINELLI

        elif message.text == 'MINELLI':
            with open('Remix/English/MINELLI/Rampampam (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  MISHLAWI

        elif message.text == 'MISHLAWI':
            with open('Remix/English/MISHLAWI/All Night (ShaHriX & JustBlack$ Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  OLIVER TREE

        elif message.text == 'OLIVER TREE':
            with open('Remix/English/OLIVER TREE/Cowboys Dont Cry (ShaHriX & UNPY Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  PHARELL WILLIAMS

        elif message.text == 'PHARELL WILLIAMS':
            with open('Remix/English/PHARELL WILLIAMS/Get Lucky (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  SEAN PAUL

        elif message.text == 'SEAN PAUL':
            with open('Remix/English/SEAN PAUL/Go Down Deh (ShaHriX & TheBlvcks Remix) (2).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/English/SEAN PAUL/No Lie (ShaHriX & Camron Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  SQUID GAME

        elif message.text == 'SQUID GAME':
            with open('Remix/English/SQUID GAME/Pink Soldiers (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  SZA

        elif message.text == 'SZA':
            with open('Remix/English/SZA/Big Boy (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  TIESTO

        elif message.text == 'TIESTO':
            with open('Remix/English/TIESTO/The Business (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  TREVOR DANIEL

        elif message.text == 'TREVOR DANIEL':
            with open('Remix/English/TREVOR DANIEL/Trevor Daniel & Selena Gomez - Past Life (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  XXXTENTACION

        elif message.text == 'XXXTENTACION':
            with open('Remix/English/XXXTENTACION/Bad (ShaHriX & JustBlack$ Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)





#  RUSSIAN REMIXES (A - Z)

    #  ADON MIX

        elif message.text == 'ADON MIX':
            with open('Remix/Russian/ADON MIX/Детка на танцполе (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  AHMED SHAD

        elif message.text == 'AHMED SHAD':
            with open('Remix/Russian/AHMED SHAD/Кристина (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  AKMAL

        elif message.text == "AKMAL'":
            with open('Remix/Russian/AKMAL/Удаляй (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  AL FAKHER

        elif message.text == 'AL FAKHER':
            with open('Remix/Russian/AL FAKHER/Музыка для души (SWERODO Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ALEKS ATAMAN

        elif message.text == 'ALEKS ATAMAN':
            with open('Remix/Russian/ALEKS ATAMAN/ОЙОЙОЙ (ТЫ ГОВОРИЛА) (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ALEKS ATAMAN/Девочка бандитка (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ALEKS ATAMAN/ОЙ ПОДЗАБЫЛИ (KXSMIC REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  AMIRCHIK

        elif message.text == 'AMIRCHIK':
            with open('Remix/Russian/AMIRCHIK/Мысли в голове (ShaHriX Remix) (2).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ANDRO

        elif message.text == "ANDRO":
            with open('Remix/Russian/ANDRO/Зари (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ANDRO/Как не любить (LUNA & ON1XX Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ANDY PANDA

        elif message.text == "ANDY PANDA":
            with open('Remix/Russian/ANDY PANDA/Marmalade (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ANDY PANDA/Буревестник (Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ANDY PANDA/Не Жалея (Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ANNA ASTI

        elif message.text == "ANNA ASTI":
            with open('Remix/Russian/ANNA ASTI/Царица (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ANNA ASTI/По барам (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  AQUARIUMS

        elif message.text == "AQUARIUMS":
            with open('Remix/Russian/AQUARIUMS/Titanic (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  AQUANEON

        elif message.text == "AQUANEON":
            with open('Remix/Russian/AQUANEON/По встречной (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/AQUANEON/Танцуй (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ARKUSHA

        elif message.text == "ARKUSHA":
            with open('Remix/Russian/ARKUSHA/Верх эгоизма (Slow_Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  AVG

        elif message.text == "AVG":
            with open('Remix/Russian/AVG/Я плачу (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/AVG/Она кайф.mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/AVG/Деам (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/AVG/Платина (ShaHriX Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/AVG/Не мороси (REMIX) (2).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/AVG/Не мороси (Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/AVG/Эй_ Братик (BERSKIY Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  BAGARDI

        elif message.text == "BAGARDI":
            with open('Remix/Russian/BAGARDI/Пам Пам (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/BAGARDI/Baby_s Dollar (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  BAKR

        elif message.text == "BAKR":
            with open('Remix/Russian/BAKR/Расстояние (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/BAKR/Вредина (Mbts Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/BAKR/За Любовь (ShaHriX Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/BAKR/Не лей (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  BITTUEV

        elif message.text == "BITTUEV":
            with open('Remix/Russian/BITTUEV/Молодой (Batishev Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  BODDIEV

        elif message.text == "BODIEV":
            with open('Remix/Russian/BODIEV/Фантом (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/BODIEV/No Pasaran (Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/BODIEV/Караван (Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  BOLIN

        elif message.text == "BOLIN":
            with open('Remix/Russian/BOLIN/Не перегори (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  BUDA

        elif message.text == "BUDA":
            with open('Remix/Russian/BUDA/Ты меня прости (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  BY ИНДИЯ

        elif message.text == "BY ИНДИЯ":
            with open('Remix/Russian/BY ИНДИЯ/Money (ShaHriX & Gloumir Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/BY ИНДИЯ/Люби меня так (Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/BY ИНДИЯ/Целуйся правильно (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  BYLIK

        elif message.text == "BYLIK":
            with open('Remix/Russian/BYLIK/Kukla (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  CHRIS YANK

        elif message.text == "CHRIS YANK":
            with open('Remix/Russian/CHRIS YANK/Холодно (Treemaine Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  CVETOCEK7

        elif message.text == "CVETOCEK7":
            with open('Remix/Russian/CVETOCEK7/Все ссоры надоели (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/CVETOCEK7/Твой Предатель (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  CYGO

        elif message.text == "CYGO":
            with open('Remix/Russian/CYGO/Panda E (Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  DANNY ABRO

        elif message.text == "DANNY ABRO":
            with open('Remix/Russian/DANNY ABRO/Салам (Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/DANNY ABRO/Время (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/DANNY ABRO/Москва не Лондон (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  DAREEM

        elif message.text == "DAREEM":
            with open('Remix/Russian/DAREEM/Новый Год (ShaHriX & TheBlvcks & NRG Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  DEESMI

        elif message.text == "DEESMI":
            with open('Remix/Russian/DEESMI/Улетали птицы (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  DIOR

        elif message.text == "DIOR":
            with open('Remix/Russian/DIOR/Фокус.mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  DJ SMASH

        elif message.text == "DJ SMASH":
            with open('Remix/Russian/DJ SMASH/Позвони.mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  DMA ILLAN

        elif message.text == "DMA ILLAN":
            with open('Remix/Russian/DMA ILLAN/Капюшон на голову (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  DZHIVAN

        elif message.text == "DZHIVAN":
            with open('Remix/Russian/DZHIVAN/Корабли (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/DZHIVAN/Автор (Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ELEY

        elif message.text == "ELEY":
            with open('Remix/Russian/ELEY/kosmos (Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ELMAN

        elif message.text == "ELMAN":
            with open('Remix/Russian/ANDRO/Зари (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ELMAN/Черная Любовь (ShaHriX Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ENRASTA

        elif message.text == "ENRASTA":
            with open('Remix/Russian/ENRASTA/Джованна (remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ESMI

        elif message.text == "ESMI":
            with open('Remix/Russian/ESMI/Выбирать чудо (UNPY REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ESCAPE

        elif message.text == "ESCAPE":
            with open('Remix/Russian/ESCAPE/Не похожи (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ESCAPE/Don_t Cry (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ESCAPE/Please don_t break my heart(KARMV REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ESCAPE/Забудь о нем (Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ESCAPE/52 Герца.mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ESCAPE/52 Герца (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ESTETIKA

        elif message.text == "ESTETIKA":
            with open('Remix/Russian/ESTETIKA/На восходе (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ETOLUBOV

        elif message.text == "ETOLUBOV":
            with open('Remix/Russian/ETOLUBOV/Притяжение (kxsmic & BERSKIY Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ETOLUBOV/Притяжение (Official remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ETOLUBOV/Притяжение (Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  GALIBRI

        elif message.text == "GALIBRI":
            with open('Remix/Russian/GALIBRI/Чак Норрис (Gatos Descarados Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  GAODAGAMO

        elif message.text == "GAODAGAMO":
            with open('Remix/Russian/GAODAGAMO/На уверенном (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  GAYAZOV$ BROTHER$

        elif message.text == "GAYAZOV$ BROTHER$":
            with open('Remix/Russian/GAYAZOV$ BROTHER$/ФАИНА (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  GENIMI

        elif message.text == "GENIMI":
            with open('Remix/Russian/GENIMI/Навсегда (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  GIDAYYAT

        elif message.text == "GIDAYYAT":
            with open('Remix/Russian/GIDAYYAT/Ядовитая (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  GRENCHANIK

        elif message.text == "GRENCHANIK":
            with open('Remix/Russian/GRENCHANIK/Девочка Плачет (Raym Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  GROOVE

        elif message.text == "GROOVE":
            with open('Remix/Russian/GROOVE/Люблю и ненавижу (Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  GUMA

        elif message.text == "GUMA":
            with open('Remix/Russian/GUMA/Не надо так (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/GUMA/Похитительница снов (Kxsmic Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/GUMA/Стеклянная (karmv REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/GUMA/Холодно (kxsmic remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  HOMIE

        elif message.text == "HOMIE":
            with open('Remix/Russian/HOMIE/Пули (Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  IDA SINGER

        elif message.text == "IDA SINGER":
            with open('Remix/Russian/IDA SINGER/РАМПАМПАМ (На русском).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  IDRIS

        elif message.text == "IDRIS":
            with open('Remix/Russian/IDRIS/Неприятели (Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  IAMMIND

        elif message.text == "IAMMIND":
            with open('Remix/Russian/IAMMIND/ONLYTATS (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  INTELLIGENT

        elif message.text == "INTELLIGENT":
            with open('Remix/Russian/INTELLIGENT/Marlboro (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  JAKONE

        elif message.text == "JAKONE":
            with open('Remix/Russian/JAKONE/По весне.mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  JAMIK

        elif message.text == "JAMIK":
            with open('Remix/Russian/JAMIK/Луи (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  JANAGA

        elif message.text == "JANAGA":
            with open('Remix/Russian/JANAGA/Малыш (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/JANAGA/В комнате мрак (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/JANAGA/Люди нелюди (Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/JANAGA/Малыш (Remix) (1).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  JAH KHALIB

        elif message.text == "JAH KHALIB":
            with open('Remix/Russian/JAH KHALIB/Доча (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  JONY

        elif message.text == "JONY":
            with open('Remix/Russian/JONY/Регресс (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/JONY/Босс (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/JONY/Давай на ты (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/JONY/На сиреневой луне (remix) (2).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/JONY/На сиреневой луне (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/JONY/Титры (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/JONY/Никак.mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  KALUSH

        elif message.text == "KALUSH":
            with open('Remix/Russian/KALUSH/Гори (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  KALVADOS

        elif message.text == "KALVADOS":
            with open('Remix/Russian/KALVADOS/Dushno (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/KALVADOS/Мама будет рада (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/KALVADOS/Мама будет рада.mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/KALVADOS/15 этаж (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/KALVADOS/Возраст (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/KALVADOS/Девочка Оскар (Dj GLAZUR Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/KALVADOS/Простыни (BERSKIY REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/KALVADOS/Простыни (karmv Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/KALVADOS/Простыни (Kxsmic Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  KAMAZZ

        elif message.text == "KAMAZZ":
            with open('Remix/Russian/KAMAZZ/Как ты там_ (Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/KAMAZZ/Принцесса (remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  KAMBULAT

        elif message.text == "KAMBULAT":
            with open('Remix/Russian/KAMBULAT/Звездопад (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/KAMBULAT/Privet (Barabanov remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/KAMBULAT/Выпей Меня (ShaHriX Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/KAMBULAT/Помоги мне (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/KAMBULAT/Привет (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/KAMBULAT/Пасмурно .mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  KARAT

        elif message.text == "KARAT":
            with open('Remix/Russian/KARAT/Танцуй малыш (BERSKIY REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  KAT-RIN

        elif message.text == "KAT-RIN":
            with open('Remix/Russian/KAT-RIN/Lambo (Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  KAVABANGA

        elif message.text == "KAVABANGA":
            with open('Remix/Russian/KAVABANGA/Рассвело (Adam Maniac remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/KAVABANGA/Так и передай ей (Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  KDK

        elif message.text == "KDK":
            with open('Remix/Russian/KDK/Отбой (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/KDK/Solnce(remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  KRISTINA SI

        elif message.text == "KRISTINA SI":
            with open('Remix/Russian/KRISTINA SI/Chem Haskanum (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  KONFUZ

        elif message.text == "KONFUZ":
            with open('Remix/Russian/KONFUZ/Выше (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/KONFUZ/Вайб ты поймала (Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/KONFUZ/Извини (SWERODO Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/KONFUZ/Рокстар (ShaHriX Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/KONFUZ/Сказка (ShaHriX & MELIX Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  LENARKO

        elif message.text == "LENARKO":
            with open('Remix/Russian/LENARKO/HQD (UNPY REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  LERA LERA

        elif message.text == "LERA LERA":
            with open('Remix/Russian/LERA LERA/Безопасный _екс (Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/LERA LERA/Безопасный кекс (BartiZ Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  LIAM HOWARD

        elif message.text == "LIAM HOWARD":
            with open('Remix/Russian/LIAM HOWARD/Нас не догонят (Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  LIL KRISTALLL

        elif message.text == "LIL KRISTALLL":
            with open('Remix/Russian/LIL KRISTALLL/Я БУДУ.mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  LIMBA

        elif message.text == "LIMBA":
            with open('Remix/Russian/LIMBA/Секрет (Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/LIMBA/Секрет (ShaHriX Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/LIMBA/Синие Фиалки (Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  LIOVA

        elif message.text == "LIOVA":
            with open('Remix/Russian/LIOVA/Всё потерял (AdonMix Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  LKN

        elif message.text == "LKN":
            with open('Remix/Russian/LKN/Как так_ (Kxsmic Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  LOOKBUFFALO

        elif message.text == "LOOKBUFFALO":
            with open('Remix/Russian/LOOKBUFFALO/Чисто Папа (BID0NCI0N & Bxston Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  LUCAVEROS

        elif message.text == "LUCAVEROS":
            with open('Remix/Russian/LUCAVEROS/Не любовь (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  LXE

        elif message.text == "LXE":
            with open('Remix/Russian/LXE/Дикий кайф (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/LXE/Замела (Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  MACAN

        elif message.text == "MACAN":
            with open('Remix/Russian/MACAN/Май (ShaHriX Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/MACAN/Поспешили (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/MACAN/IVL (ShaHriX Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/MACAN/ASPHALT 8 (ShaHriX Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/MACAN/Big City Life (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/MACAN/Плачь_ но не звони.mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/MACAN/За всех (Remix) (2).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/MACAN/За всех (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/MACAN/Останься образом (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  MADURI

        elif message.text == "MADURI":
            with open('Remix/Russian/MADURI/Стреляй.mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  MARKUL

        elif message.text == "MARKUL":
            with open('Remix/Russian/MARKUL/Стрелы (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  MATLY

        elif message.text == "MATLY":
            with open('Remix/Russian/MATLY/ты похож на кота (Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  MAYOT

        elif message.text == "MAYOT":
            with open('Remix/Russian/MAYOT/4_30.mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/MAYOT/Море (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  MEALON

        elif message.text == "MEALON":
            with open('Remix/Russian/MEALON/Молодым (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  MEKHMAN

        elif message.text == "MEKHMAN":
            with open('Remix/Russian/MEKHMAN/Эскобар.mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  MIYAGI

        elif message.text == "MIYAGI":
            with open('Remix/Russian/MIYAGI/Временно (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/MIYAGI/Ночь (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/MIYAGI/Silhouette (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/MIYAGI/Ночь .mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/MIYAGI/Marmalade (ShaHriX Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/MIYAGI/Буревестник (Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/MIYAGI/Не Жалея (Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  MR LAMBO

        elif message.text == "MR LAMBO":
            with open('Remix/Russian/MR LAMBO/Чилим (ShaHriX Remix.mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/MR LAMBO/Shuttle (UNPY REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  NASTY BABE

        elif message.text == "NASTY BABE":
            with open('Remix/Russian/NASTY BABE/По глазам (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  NECHAEV

        elif message.text == "NECHAEV":
            with open('Remix/Russian/NECHAEV/Беги (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  NEEL

        elif message.text == "NEEL":
            with open('Remix/Russian/NEEL/BLACKBERRY (Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/NEEL/Мона Лиза (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  NECOGLAI

        elif message.text == "NEKOGLAI":
            with open('Remix/Russian/NEKOGLAI/Cumback (Arch Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/NEKOGLAI/Cumback (Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  NICENIGHT

        elif message.text == "NICENIGHT":
            with open('Remix/Russian/NICENIGHT/Небо будто вата (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  NIKITATA

        elif message.text == "NIKITATA":
            with open('Remix/Russian/NIKITATA/Спать без тебя (Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  NLO

        elif message.text == "NLO":
            with open('Remix/Russian/NLO/Девочка морока (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/NLO/Плюшевый (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/NLO/Синий джин (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/NLO/Холодный космос (Kxsmic Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  NVRKN134

        elif message.text == "NVRKN134":
            with open('Remix/Russian/NVRKN134/Ты Не Королева (SWERODO Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  NЮ

        elif message.text == "NЮ":
            with open('Remix/Russian/NЮ/NЮ - Никто (BERSKIY Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ODGO

        elif message.text == "ODGO":
            with open('Remix/Russian/ODGO/ТЫ МОЙ ЯД.mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  OXXXYMIRON

        elif message.text == "OXXXYMIRON":
            with open('Remix/Russian/OXXXYMIRON/THE STORY OF ALISHER.mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  PUSSYKILLER

        elif message.text == "PUSSYKILLER":
            with open('Remix/Russian/PUSSYKILLER/Одним выстрелом (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  QYAL QYAL

        elif message.text == "QYAL QYAL":
            with open('Remix/Russian/QYAL QYAL/Мурашки (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  R.RICCADO

        elif message.text == "R.RICCADO":
            with open('Remix/Russian/R.RICCADO/Ну привет (REMIX) .mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/R.RICCADO/Никогда (Karmv Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  RAIKAHO

        elif message.text == "RAIKAHO":
            with open('Remix/Russian/RAIKAHO/Девочка Наркотик (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/RAIKAHO/Подшофе (SWERODO Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  RAKHIM

        elif message.text == "RAKHIM":
            with open('Remix/Russian/RAKHIM/Аккорды (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  RAMIL

        elif message.text == "RAMIL":
            with open('Remix/Russian/RAMIL/Убей Меня (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/RAMIL/Просто лети (Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/RAMIL/MP3 (FriDrix Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/RAMIL/MP3 (ShaHriX Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/RAMIL/Маяк (ShaHriX & FriDrix Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/RAMIL/Не ищи меня (Miki Mouse Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/RAMIL/Убей Меня (Fandi Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/RAMIL/Убей Меня (Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/RAMIL/Увидимся (ShaHriX Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  RASA

        elif message.text == "RASA":
            with open('Remix/Russian/RASA/Фиолетово (UNPY REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/RASA/Offline(REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/RASA/ПОГУДИМ (kxsmic REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  REAL GIRL

        elif message.text == "REAL GIRL":
            with open('Remix/Russian/REAL GIRL/Отпускаю (Cover) (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  SAM WICK

        elif message.text == "SAM WICK":
            with open('Remix/Russian/SAM WICK/Пойми (Subrik Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  SANTY ONE

        elif message.text == "SANTY ONE":
            with open('Remix/Russian/SANTY ONE/Я с тобой (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  SANTIZ

        elif message.text == "SANTIZ":
            with open('Remix/Russian/SANTIZ/Посмотри назад (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  SASHA SANTA

        elif message.text == "SASHA SANTA":
            with open('Remix/Russian/SASHA SANTA/Кавычки (kxsmic remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/SASHA SANTA/18_ (Karmv Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/SASHA SANTA/18_ (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/SASHA SANTA/В душу (Karmv Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  SCIRENA

        elif message.text == "SCIRENA":
            with open('Remix/Russian/SCIRENA/Деньги и Москва (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  SHAMI

        elif message.text == "SHAMI":
            with open('Remix/Russian/SHAMI/Она ищет любовь (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  SHEIKH MANSUR

        elif message.text == "SHEIKH MANSUR":
            with open('Remix/Russian/SHEIKH MANSUR/Балдини (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  SLAVA MARLOW

        elif message.text == "SLAVA MARLOW":
            with open('Remix/Russian/SLAVA MARLOW/Ты далеко (Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  SLAVIK POGOSOV

        elif message.text == "SLAVIK POGOSOV":
            with open('Remix/Russian/SLAVIK POGOSOV/Монро (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/SLAVIK POGOSOV/Монро (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/SLAVIK POGOSOV/Монро.mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  STRANGE

        elif message.text == "STRANGE":
            with open('Remix/Russian/STRANGE/Зависай (BERSKIY Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  STRCTRE

        elif message.text == "STRCTRE":
            with open('Remix/Russian/STRCTRE/Дай огня (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  T1ONE

        elif message.text == "T1ONE":
            with open('Remix/Russian/T1ONE/Вино Помогает (Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  TARAS

        elif message.text == "TARAS":
            with open('Remix/Russian/TARAS/Моя девочка (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  TANIR

        elif message.text == "TANIR":
            with open('Remix/Russian/TANIR/Мама это ночь (Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/TANIR/Аккуратно (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/TANIR/Пуля (karmv remix) (2).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/TANIR/Пуля (KARMV REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  TESLYA

        elif message.text == "TESLYA":
            with open('Remix/Russian/TESLYA/Mercedes (SWERODO Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/TESLYA/Летать (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  TIMRAN

        elif message.text == "TIMRAN":
            with open('Remix/Russian/TIMRAN/Не пускайте танцевать (Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  TINI LIN

        elif message.text == "TINI LIN":
            with open('Remix/Russian/TINI LIN/Последний танец (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    # TORI KVIT

        elif message.text == "TORI KVIT":
            with open('Remix/Russian/TORI KVIT/Девочка (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  V$XV PRINCE

        elif message.text == "V$XV PRINCE":
            with open('Remix/Russian/V$XV PRINCE/Суета (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  VERBEE

        elif message.text == "VERBEE":
            with open('Remix/Russian/VERBEE/Ясный мой свет.mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  VESNA305

        elif message.text == "VESNA305":
            with open('Remix/Russian/VESNA305/Новый год.mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  WELLAY

        elif message.text == "WELLAY":
            with open('Remix/Russian/WELLAY/Танцуй (Remix) (2).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  WHITE GALLOWS

        elif message.text == "WHITE GALLOWS":
            with open('Remix/Russian/WHITE GALLOWS/Призрак.mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/WHITE GALLOWS/Королева бала (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  WHYBABY

        elif message.text == "WHYBABY":
            with open('Remix/Russian/WHYBABY/Paypass (karmv remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  X

        elif message.text == "X":
            with open('Remix/Russian/X/Play.mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  XASSA

        elif message.text == "XASSA":
            with open('Remix/Russian/XASSA/Beautiful Life (Kxsmic & Alexei Shkurko Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/XASSA/Paradise (SWERODO Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/XASSA/Влюбилась в дурака (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/XASSA/Романтик (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  XCHO

        elif message.text == "XCHO":
            with open('Remix/Russian/XCHO/Ты и я (8D REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/XCHO/Вороны (remix) (2).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/XCHO/Вороны (Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/XCHO/Закрыла даль (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/XCHO/Закрыла даль (SWERODO Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/XCHO/Мой мир (Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/XCHO/Про любовь (SWERODO Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/XCHO/Ты и я (Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/XCHO/Где же вы (SLOWED).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  XOLIDAYBOY

        elif message.text == "XOLIDAYBOY":
            with open('Remix/Russian/XOLIDAYBOY/Моя хулиганка (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  YACHEVSKIY

        elif message.text == "YACHEVSKIY":
            with open('Remix/Russian/YACHEVSKIY/BRABUS (BERSKIY REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  YUFOLL

        elif message.text == "YUFOLL":
            with open('Remix/Russian/YUFOLL/В белом платье (Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ZIPPO

        elif message.text == "ZIPPO":
            with open('Remix/Russian/ZIPPO/Остаток слов (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ZOMB

        elif message.text == "ZOMB":
            with open('Remix/Russian/ZOMB/BABY TONIGHT.mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ZOMB/Пантомима (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ZOMB/Селяви (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)










#  RUSSIAN REMIXES (А - Я)  #

    #  АБРИКОСА

        elif message.text == "АБРИКОСА":
            with open('Remix/Russian/АБРИКОСА/Бюджет (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  АДВАЙТА

        elif message.text == "АДВАЙТА":
            with open('Remix/Russian/АДВАЙТА/Ocean (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  АРКАЙДА

        elif message.text == "АРКАЙДА":
            with open('Remix/Russian/АРКАЙДА/С горем да пополам (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/АРКАЙДА/Глупая полюбила.mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/АРКАЙДА/Дай Дыма Брат (ShaHriX Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/АРКАЙДА/Теперь вали (Silver Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  АНДРЕЙ ЛЕНИЦКИЙ

        elif message.text == "АНДРЕЙ ЛЕНИЦКИЙ":
            with open('Remix/Russian/АНДРЕЙ ЛЕНИЦКИЙ/Другой (AdonMix Edit).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  АЛЁНА ШВЕЦ.

        elif message.text == "АЛЁНА ШВЕЦ.":
            with open('Remix/Russian/АЛЁНА ШВЕЦ/Вино_и_Сигареты_Real_Girl_Cover_ShaHriX_Remix.mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  АМУРА

        elif message.text == "АМУРА":
            with open('Remix/Russian/АМУРА/Минимум (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/АМУРА/Спрячься (Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  БОДЯ МИР642

        elif message.text == "БОДЯ МИР642":
            with open('Remix/Russian/БОДЯ МИР642/Meloman (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ВАНЯ ДМИТРЕНКО

        elif message.text == "ВАНЯ ДМИТРЕНКО":
            with open('Remix/Russian/ВАНЯ ДМИТРЕНКО/Лего (Mikis Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ВСЕГДА МЕЧТАЛ

        elif message.text == "ВСЕГДА МЕЧТАЛ":
            with open('Remix/Russian/ВСЕГДАМЕЧТАЛ/Синабон (Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ГАНВЕСТ

        elif message.text == "ГАНВЕСТ":
            with open('Remix/Russian/ГАНВЕСТ/Ты такая GLE (BERSKIY Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ДЕНИС RIDER

        elif message.text == "ДЕНИС RIDER":
            with open('Remix/Russian/ДЕНИС RIDER/Перейдем на ты (kxsmic remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ДЖАЯММИ

        elif message.text == "ДЖАЯММИ":
            with open('Remix/Russian/ДЖАЯММИ/По полям (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ДЖИОС

        elif message.text == "ДЖИОС":
            with open('Remix/Russian/ДЖИОС/Тело (kxsmic remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ДЖИОС/Умотан (KARMV RMX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ЕГОР КРИД

        elif message.text == "ЕГОР КРИД":
            with open('Remix/Russian/ЕГОР КРИД/WE GOTTA GET LOVE (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ЕГОР КРИД/We Gotta Get Love (ShaHriX Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ЕГОР КРИД/Отпускаю (ShaHriX Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ЕГОР КРИД/3-е Сентября (UNPY REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ЕГОР КРИД/3-е Cентября.mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ИНТЕРНАЛ

        elif message.text == "ИНТЕРНАЛ":
            with open('Remix/Russian/ИНТЕРНАЛ/Заболел_ но не тобой (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ИСЛАМ ИТЛЯШЕВ

        elif message.text == "ИСЛАМ ИТЛЯШЕВ":
            with open('Remix/Russian/ИСЛАМ ИТЛЯШЕВ/НА РАХАТЕ (Kxsmic Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  КАНГИ

        elif message.text == "КАНГИ":
            with open('Remix/Russian/КАНГИ/Голова (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/КАНГИ/Голова.mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  КАСПИЙСКИЙ ГРУЗ

        elif message.text == "КАСПИЙСКИЙ ГРУЗ":
            with open('Remix/Russian/КАСПИЙСКИЙ ГРУЗ/На белом (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/КАСПИЙСКИЙ ГРУЗ/18_ (REMIX) (2).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ЛЁША СВИК

        elif message.text == "ЛЁША СВИК":
            with open('Remix/Russian/ЛЁША СВИК/Плакала (Remix) (2).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ЛЁША СВИК/Плакала (Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ЛИВИ

        elif message.text == "ЛИВИ":
            with open('Remix/Russian/ЛИВИ/Влюблён (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ЛЫФАРЬ

        elif message.text == "ЛЫФАРЬ":
            with open('Remix/Russian/ЛЫФАРЬ/Техно (KARMV REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  МАКС КОРЖ

        elif message.text == "МАКС КОРЖ":
            with open('Remix/Russian/МАКС КОРЖ/Не твой (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  МАЛЬБЕК

        elif message.text == "МАЛЬБЕК":
            with open('Remix/Russian/МАЛЬБЕК/Равнодушие (UNPY REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  МИЧЕЛЗ

        elif message.text == "МИЧЕЛЗ":
            with open('Remix/Russian/МИЧЕЛЗ/Она Хочет (kxsmic remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  МОТ

        elif message.text == "МОТ":
            with open('Remix/Russian/МОТ/Август - это ты (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  НИКУБА

        elif message.text == "НИКУБА":
            with open('Remix/Russian/НИКУБА/Мы в порше (Karmv Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ОСТАП ПАРФЁНОВ

        elif message.text == "ОСТАП ПАРФЁНОВ":
            with open('Remix/Russian/ОСТАП ПАРФЁНОВ/Джингл Белс не будет.mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ОСТАП ПАРФЁНОВ/Ты не королева (BERSKIY Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ОСТАП ПАРФЁНОВ/ТЫ НЕ КОРОЛЕВА (Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ПАША PROOROK

        elif message.text == "ПАША PROOROK":
            with open('Remix/Russian/ПАША PROOROK/А любви нашей хана (RENDOW Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ПЛАГА

        elif message.text == "ПЛАГА":
            with open('Remix/Russian/ПЛАГА/Туман.mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ПЛАГА/Раньше (Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ПОШЛЫЙ

        elif message.text == "ПОШЛЫЙ":
            with open('Remix/Russian/ПОШЛЫЙ/Колейдоскоп (Karmv Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  СКРИПТОНИТ

        elif message.text == "СКРИПТОНИТ":
            with open('Remix/Russian/СКРИПТОНИТ/Slow Mo.mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  СУЛТАН ЛАГУЧЕВ

        elif message.text == "СУЛТАН ЛАГУЧЕВ":
            with open('Remix/Russian/СУЛТАН ЛАГУЧЕВ/Не Души (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ТИМА АКИМОВ

        elif message.text == "ТИМА АКИМОВ":
            with open('Remix/Russian/ТИМА АКИМОВ/Пролетело лето.mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ТИМА БЕЛОРУССКИХ

        elif message.text == "ТИМА БЕЛОРУССКИХ":
            with open('Remix/Russian/ТИМА БЕЛОРУССКИХ/Я Больше Не Напишу (Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ТРИ ДНЯ ДОЖДЯ

        elif message.text == "ТРИ ДНЯ ДОЖДЯ":
            with open('Remix/Russian/ТРИ ДНЯ ДОЖДЯ/Я и одиночество (Rendow Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ФЛИТ

        elif message.text == "ФЛИТ":
            with open('Remix/Russian/ФЛИТ/Малиновое небо (karmv Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ФОГЕЛЬ

        elif message.text == "ФОГЕЛЬ":
            with open('Remix/Russian/ФОГЕЛЬ/СТЕРВА (Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ШЕЙХ МАНСУР

        elif message.text == "ШЕЙХ МАНСУР":
            with open('Remix/Russian/ШЕЙХ МАНСУР/Соврал (Karmv & AdonMix Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ЭЛДЖЕЙ

        elif message.text == "ЭЛДЖЕЙ":
            with open('Remix/Russian/ЭЛДЖЕЙ/Harakiri (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ЭЛДЖЕЙ/Бронежилет (ShaHriX Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ЭНШПИЛЬ

        elif message.text == "ЭНДШПИЛЬ":
            with open('Remix/Russian/ЭНДШПИЛЬ/Туда (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ЭНДШПИЛЬ/Капканы .mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ЭНДШПИЛЬ/Приятная (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ЭРИКА ЛУНДМОЕН

        elif message.text == "ЭРИКА ЛУНДМОЕН":
            with open('Remix/Russian/ЭРИКА ЛУНДМОЕН/Яд (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ЮЛИАНА КАРАУЛОВА

        elif message.text == "ЮЛИАНА КАРАУЛОВА":
            with open('Remix/Russian/ЮЛИАНА КАРАУЛОВА/Ты не такой (Kxsmic REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ЮРИЙ ШАТУНОВ

        elif message.text == "ЮРИЙ ШАТУНОВ":
            with open('Remix/Russian/ЮРИЙ ШАТУНОВ/Забудь (SWERODO Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ЮРИЙ ШАТУНОВ/Седая Ночь (Cvetocek7 Cover) (ShaHriX Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ЯД ДОБРА

        elif message.text == "ЯД ДОБРА":
            with open('Remix/Russian/ЯД ДОБРА/Банда (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ЯМЫЧ

        elif message.text == "ЯМЫЧ":
            with open('Remix/Russian/ЯМЫЧ/Чёрный BMW (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  84

        elif message.text == "84":
            with open('Remix/Russian/84/Классная.mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  3-ИЙ ЯНВАРЬ

        elif message.text == "3-ИЙ ЯНВАРЬ":
            with open('Remix/Russian/3-ИЙ ЯНВАРЬ/Переходный возраст (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  5УТРА

        elif message.text == "5УТРА":
            with open('Remix/Russian/5УТРА/Давай сбежим (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/5УТРА/Без_тебя_я_тону_в_этом_море_Barabanov_Remix.mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  100ЛИЦЯ

        elif message.text == "100ЛИЦЯ":
            with open('Remix/Russian/100ЛИЦЯ/Чорнобрива (KARMV Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    else:
        await bot.send_message(message.chat.id, '<b> Чтобы пользоваться ботом, подпишитесь на наши каналы ❗️ </b>', parse_mode = 'html', reply_markup = inline_markups.subscribe_inline)














#  SEARCH

@dp.message_handler(state = SearchState.search)
async def search_audio(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['search'] = message.text
        message.text = str.upper(message.text)

    #  CANCEL

        if message.text == 'ОТМЕНИТЬ':
            await bot.send_message(message.chat.id, '<b> Поиск отменён. </b>', parse_mode = 'html', reply_markup = reply_markups.menu_reply)
            await delete_message_1(message)
            await state.finish()

    #  BLACKBEAR

        elif message.text == 'BLACKBEAR':
            with open('Remix/English/BLACKBEAR/blackbear - idfc [aibek berkimbaev & shahrix remix].mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  CASSETTE

        elif message.text == 'CASSETTE':
            with open('Remix/English/CASSETTE/My Way (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  DAFT PUNK

        elif message.text == 'DAFT PUNK':
            with open('Remix/English/DAFT PUNK/Get Lucky (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  DUA LIPA

        elif message.text == 'DUA LIPA':
            with open('Remix/English/DUA LIPA/No Lie (ShaHriX & Camron Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  FOUSHEE

        elif message.text == 'FOUSHEE':
            with open('Remix/English/FOUSHEE/Deep End (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  G-EASY

        elif message.text == 'G-EASY':
            with open('Remix/English/G-EASY/Him & I (ShaHriX & Melix Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  GHOSTLY KISSES

        elif message.text == 'GHOSTLY KISSES':
            with open('Remix/English/GHOSTLY KISSES/Ghostly_Kisses_Empty_Note_Aibek_Berkimbaev_&_ShaHriX_remix.mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  IAN STORM

        elif message.text == 'IAN STORM':
            with open('Remix/English/IAN STORM/Run Away (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  INNA

        elif message.text == 'INNA':
            with open('Remix/English/INNA/Lonely (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/English/INNA/Solo (ShaHriX Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  JVLA

        elif message.text == 'JVLA':
            with open('Remix/English/JVLA/Such A Whole Remix.mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  KINA

        elif message.text == 'KINA':
            with open('Remix/English/KINA/Kina - Get You The Moon (ShaHriX & Amalee Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  LADY GAGA

        elif message.text == 'LADY GAGA':
            with open('Remix/English/LADY GAGA/Bloody Mary (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  LISA

        elif message.text == 'LISA':
            with open('Remix/English/LISA/Money (ShaHriX & TheBlvcks  Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  MINELLI

        elif message.text == 'MINELLI':
            with open('Remix/English/MINELLI/Rampampam (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  MISHLAWI

        elif message.text == 'MISHLAWI':
            with open('Remix/English/MISHLAWI/All Night (ShaHriX & JustBlack$ Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  OLIVER TREE

        elif message.text == 'OLIVER TREE':
            with open('Remix/English/OLIVER TREE/Cowboys Dont Cry (ShaHriX & UNPY Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  PHARELL WILLIAMS

        elif message.text == 'PHARELL WILLIAMS':
            with open('Remix/English/PHARELL WILLIAMS/Get Lucky (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  SEAN PAUL

        elif message.text == 'SEAN PAUL':
            with open('Remix/English/SEAN PAUL/Go Down Deh (ShaHriX & TheBlvcks Remix) (2).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/English/SEAN PAUL/No Lie (ShaHriX & Camron Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  SQUID GAME

        elif message.text == 'SQUID GAME':
            with open('Remix/English/SQUID GAME/Pink Soldiers (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  SZA

        elif message.text == 'SZA':
            with open('Remix/English/SZA/Big Boy (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  TIESTO

        elif message.text == 'TIESTO':
            with open('Remix/English/TIESTO/The Business (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  TREVOR DANIEL

        elif message.text == 'TREVOR DANIEL':
            with open('Remix/English/TREVOR DANIEL/Trevor Daniel & Selena Gomez - Past Life (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  XXXTENTACION

        elif message.text == 'XXXTENTACION':
            with open('Remix/English/XXXTENTACION/Bad (ShaHriX & JustBlack$ Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)





#  RUSSIAN REMIXES (A - Z)

    #  ADON MIX

        elif message.text == 'ADON MIX':
            with open('Remix/Russian/ADON MIX/Детка на танцполе (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  AHMED SHAD

        elif message.text == 'AHMED SHAD':
            with open('Remix/Russian/AHMED SHAD/Кристина (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  AKMAL

        elif message.text == "AKMAL'":
            with open('Remix/Russian/AKMAL/Удаляй (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  AL FAKHER

        elif message.text == 'AL FAKHER':
            with open('Remix/Russian/AL FAKHER/Музыка для души (SWERODO Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ALEKS ATAMAN

        elif message.text == 'ALEKS ATAMAN':
            with open('Remix/Russian/ALEKS ATAMAN/ОЙОЙОЙ (ТЫ ГОВОРИЛА) (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ALEKS ATAMAN/Девочка бандитка (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ALEKS ATAMAN/ОЙ ПОДЗАБЫЛИ (KXSMIC REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  AMIRCHIK

        elif message.text == 'AMIRCHIK':
            with open('Remix/Russian/AMIRCHIK/Мысли в голове (ShaHriX Remix) (2).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ANDRO

        elif message.text == "ANDRO":
            with open('Remix/Russian/ANDRO/Зари (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ANDRO/Как не любить (LUNA & ON1XX Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ANDY PANDA

        elif message.text == "ANDY PANDA":
            with open('Remix/Russian/ANDY PANDA/Marmalade (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ANDY PANDA/Буревестник (Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ANDY PANDA/Не Жалея (Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ANNA ASTI

        elif message.text == "ANNA ASTI":
            with open('Remix/Russian/ANNA ASTI/Царица (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ANNA ASTI/По барам (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  AQUARIUMS

        elif message.text == "AQUARIUMS":
            with open('Remix/Russian/AQUARIUMS/Titanic (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  AQUANEON

        elif message.text == "AQUANEON":
            with open('Remix/Russian/AQUANEON/По встречной (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/AQUANEON/Танцуй (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ARKUSHA

        elif message.text == "ARKUSHA":
            with open('Remix/Russian/ARKUSHA/Верх эгоизма (Slow_Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  AVG

        elif message.text == "AVG":
            with open('Remix/Russian/AVG/Я плачу (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/AVG/Она кайф.mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/AVG/Деам (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/AVG/Платина (ShaHriX Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/AVG/Не мороси (REMIX) (2).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/AVG/Не мороси (Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/AVG/Эй_ Братик (BERSKIY Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  BAGARDI

        elif message.text == "BAGARDI":
            with open('Remix/Russian/BAGARDI/Пам Пам (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/BAGARDI/Baby_s Dollar (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  BAKR

        elif message.text == "BAKR":
            with open('Remix/Russian/BAKR/Расстояние (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/BAKR/Вредина (Mbts Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/BAKR/За Любовь (ShaHriX Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/BAKR/Не лей (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  BITTUEV

        elif message.text == "BITTUEV":
            with open('Remix/Russian/BITTUEV/Молодой (Batishev Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  BODDIEV

        elif message.text == "BODIEV":
            with open('Remix/Russian/BODIEV/Фантом (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/BODIEV/No Pasaran (Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/BODIEV/Караван (Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  BOLIN

        elif message.text == "BOLIN":
            with open('Remix/Russian/BOLIN/Не перегори (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  BUDA

        elif message.text == "BUDA":
            with open('Remix/Russian/BUDA/Ты меня прости (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  BY ИНДИЯ

        elif message.text == "BY ИНДИЯ":
            with open('Remix/Russian/BY ИНДИЯ/Money (ShaHriX & Gloumir Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/BY ИНДИЯ/Люби меня так (Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/BY ИНДИЯ/Целуйся правильно (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  BYLIK

        elif message.text == "BYLIK":
            with open('Remix/Russian/BYLIK/Kukla (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  CHRIS YANK

        elif message.text == "CHRIS YANK":
            with open('Remix/Russian/CHRIS YANK/Холодно (Treemaine Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  CVETOCEK7

        elif message.text == "CVETOCEK7":
            with open('Remix/Russian/CVETOCEK7/Все ссоры надоели (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/CVETOCEK7/Твой Предатель (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  CYGO

        elif message.text == "CYGO":
            with open('Remix/Russian/CYGO/Panda E (Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  DANNY ABRO

        elif message.text == "DANNY ABRO":
            with open('Remix/Russian/DANNY ABRO/Салам (Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/DANNY ABRO/Время (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/DANNY ABRO/Москва не Лондон (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  DAREEM

        elif message.text == "DAREEM":
            with open('Remix/Russian/DAREEM/Новый Год (ShaHriX & TheBlvcks & NRG Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  DEESMI

        elif message.text == "DEESMI":
            with open('Remix/Russian/DEESMI/Улетали птицы (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  DIOR

        elif message.text == "DIOR":
            with open('Remix/Russian/DIOR/Фокус.mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  DJ SMASH

        elif message.text == "DJ SMASH":
            with open('Remix/Russian/DJ SMASH/Позвони.mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  DMA ILLAN

        elif message.text == "DMA ILLAN":
            with open('Remix/Russian/DMA ILLAN/Капюшон на голову (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  DZHIVAN

        elif message.text == "DZHIVAN":
            with open('Remix/Russian/DZHIVAN/Корабли (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/DZHIVAN/Автор (Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ELEY

        elif message.text == "ELEY":
            with open('Remix/Russian/ELEY/kosmos (Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ELMAN

        elif message.text == "ELMAN":
            with open('Remix/Russian/ANDRO/Зари (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ELMAN/Черная Любовь (ShaHriX Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ENRASTA

        elif message.text == "ENRASTA":
            with open('Remix/Russian/ENRASTA/Джованна (remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ESMI

        elif message.text == "ESMI":
            with open('Remix/Russian/ESMI/Выбирать чудо (UNPY REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ESCAPE

        elif message.text == "ESCAPE":
            with open('Remix/Russian/ESCAPE/Не похожи (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ESCAPE/Don_t Cry (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ESCAPE/Please don_t break my heart(KARMV REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ESCAPE/Забудь о нем (Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ESCAPE/52 Герца.mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ESCAPE/52 Герца (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ESTETIKA

        elif message.text == "ESTETIKA":
            with open('Remix/Russian/ESTETIKA/На восходе (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ETOLUBOV

        elif message.text == "ETOLUBOV":
            with open('Remix/Russian/ETOLUBOV/Притяжение (kxsmic & BERSKIY Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ETOLUBOV/Притяжение (Official remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ETOLUBOV/Притяжение (Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  GALIBRI

        elif message.text == "GALIBRI":
            with open('Remix/Russian/GALIBRI/Чак Норрис (Gatos Descarados Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  GAODAGAMO

        elif message.text == "GAODAGAMO":
            with open('Remix/Russian/GAODAGAMO/На уверенном (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  GAYAZOV$ BROTHER$

        elif message.text == "GAYAZOV$ BROTHER$":
            with open('Remix/Russian/GAYAZOV$ BROTHER$/ФАИНА (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  GENIMI

        elif message.text == "GENIMI":
            with open('Remix/Russian/GENIMI/Навсегда (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  GIDAYYAT

        elif message.text == "GIDAYYAT":
            with open('Remix/Russian/GIDAYYAT/Ядовитая (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  GRENCHANIK

        elif message.text == "GRENCHANIK":
            with open('Remix/Russian/GRENCHANIK/Девочка Плачет (Raym Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  GROOVE

        elif message.text == "GROOVE":
            with open('Remix/Russian/GROOVE/Люблю и ненавижу (Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  GUMA

        elif message.text == "GUMA":
            with open('Remix/Russian/GUMA/Не надо так (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/GUMA/Похитительница снов (Kxsmic Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/GUMA/Стеклянная (karmv REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/GUMA/Холодно (kxsmic remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  HOMIE

        elif message.text == "HOMIE":
            with open('Remix/Russian/HOMIE/Пули (Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  IDA SINGER

        elif message.text == "IDA SINGER":
            with open('Remix/Russian/IDA SINGER/РАМПАМПАМ (На русском).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  IDRIS

        elif message.text == "IDRIS":
            with open('Remix/Russian/IDRIS/Неприятели (Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  IAMMIND

        elif message.text == "IAMMIND":
            with open('Remix/Russian/IAMMIND/ONLYTATS (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  INTELLIGENT

        elif message.text == "INTELLIGENT":
            with open('Remix/Russian/INTELLIGENT/Marlboro (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  JAKONE

        elif message.text == "JAKONE":
            with open('Remix/Russian/JAKONE/По весне.mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  JAMIK

        elif message.text == "JAMIK":
            with open('Remix/Russian/JAMIK/Луи (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  JANAGA

        elif message.text == "JANAGA":
            with open('Remix/Russian/JANAGA/Малыш (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/JANAGA/В комнате мрак (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/JANAGA/Люди нелюди (Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/JANAGA/Малыш (Remix) (1).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  JAH KHALIB

        elif message.text == "JAH KHALIB":
            with open('Remix/Russian/JAH KHALIB/Доча (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  JONY

        elif message.text == "JONY":
            with open('Remix/Russian/JONY/Регресс (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/JONY/Босс (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/JONY/Давай на ты (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/JONY/На сиреневой луне (remix) (2).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/JONY/На сиреневой луне (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/JONY/Титры (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/JONY/Никак.mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  KALUSH

        elif message.text == "KALUSH":
            with open('Remix/Russian/KALUSH/Гори (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  KALVADOS

        elif message.text == "KALVADOS":
            with open('Remix/Russian/KALVADOS/Dushno (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/KALVADOS/Мама будет рада (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/KALVADOS/Мама будет рада.mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/KALVADOS/15 этаж (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/KALVADOS/Возраст (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/KALVADOS/Девочка Оскар (Dj GLAZUR Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/KALVADOS/Простыни (BERSKIY REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/KALVADOS/Простыни (karmv Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/KALVADOS/Простыни (Kxsmic Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  KAMAZZ

        elif message.text == "KAMAZZ":
            with open('Remix/Russian/KAMAZZ/Как ты там_ (Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/KAMAZZ/Принцесса (remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  KAMBULAT

        elif message.text == "KAMBULAT":
            with open('Remix/Russian/KAMBULAT/Звездопад (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/KAMBULAT/Privet (Barabanov remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/KAMBULAT/Выпей Меня (ShaHriX Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/KAMBULAT/Помоги мне (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/KAMBULAT/Привет (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/KAMBULAT/Пасмурно .mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  KARAT

        elif message.text == "KARAT":
            with open('Remix/Russian/KARAT/Танцуй малыш (BERSKIY REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  KAT-RIN

        elif message.text == "KAT-RIN":
            with open('Remix/Russian/KAT-RIN/Lambo (Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  KAVABANGA

        elif message.text == "KAVABANGA":
            with open('Remix/Russian/KAVABANGA/Рассвело (Adam Maniac remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/KAVABANGA/Так и передай ей (Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  KDK

        elif message.text == "KDK":
            with open('Remix/Russian/KDK/Отбой (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/KDK/Solnce(remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  KRISTINA SI

        elif message.text == "KRISTINA SI":
            with open('Remix/Russian/KRISTINA SI/Chem Haskanum (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  KONFUZ

        elif message.text == "KONFUZ":
            with open('Remix/Russian/KONFUZ/Выше (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/KONFUZ/Вайб ты поймала (Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/KONFUZ/Извини (SWERODO Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/KONFUZ/Рокстар (ShaHriX Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/KONFUZ/Сказка (ShaHriX & MELIX Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  LENARKO

        elif message.text == "LENARKO":
            with open('Remix/Russian/LENARKO/HQD (UNPY REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  LERA LERA

        elif message.text == "LERA LERA":
            with open('Remix/Russian/LERA LERA/Безопасный _екс (Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/LERA LERA/Безопасный кекс (BartiZ Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  LIAM HOWARD

        elif message.text == "LIAM HOWARD":
            with open('Remix/Russian/LIAM HOWARD/Нас не догонят (Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  LIL KRISTALLL

        elif message.text == "LIL KRISTALLL":
            with open('Remix/Russian/LIL KRISTALLL/Я БУДУ.mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  LIMBA

        elif message.text == "LIMBA":
            with open('Remix/Russian/LIMBA/Секрет (Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/LIMBA/Секрет (ShaHriX Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/LIMBA/Синие Фиалки (Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  LIOVA

        elif message.text == "LIOVA":
            with open('Remix/Russian/LIOVA/Всё потерял (AdonMix Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  LKN

        elif message.text == "LKN":
            with open('Remix/Russian/LKN/Как так_ (Kxsmic Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  LOOKBUFFALO

        elif message.text == "LOOKBUFFALO":
            with open('Remix/Russian/LOOKBUFFALO/Чисто Папа (BID0NCI0N & Bxston Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  LUCAVEROS

        elif message.text == "LUCAVEROS":
            with open('Remix/Russian/LUCAVEROS/Не любовь (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  LXE

        elif message.text == "LXE":
            with open('Remix/Russian/LXE/Дикий кайф (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/LXE/Замела (Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  MACAN

        elif message.text == "MACAN":
            with open('Remix/Russian/MACAN/Май (ShaHriX Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/MACAN/Поспешили (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/MACAN/IVL (ShaHriX Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/MACAN/ASPHALT 8 (ShaHriX Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/MACAN/Big City Life (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/MACAN/Плачь_ но не звони.mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/MACAN/За всех (Remix) (2).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/MACAN/За всех (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/MACAN/Останься образом (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  MADURI

        elif message.text == "MADURI":
            with open('Remix/Russian/MADURI/Стреляй.mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  MARKUL

        elif message.text == "MARKUL":
            with open('Remix/Russian/MARKUL/Стрелы (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  MATLY

        elif message.text == "MATLY":
            with open('Remix/Russian/MATLY/ты похож на кота (Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  MAYOT

        elif message.text == "MAYOT":
            with open('Remix/Russian/MAYOT/4_30.mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/MAYOT/Море (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  MEALON

        elif message.text == "MEALON":
            with open('Remix/Russian/MEALON/Молодым (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  MEKHMAN

        elif message.text == "MEKHMAN":
            with open('Remix/Russian/MEKHMAN/Эскобар.mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  MIYAGI

        elif message.text == "MIYAGI":
            with open('Remix/Russian/MIYAGI/Временно (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/MIYAGI/Ночь (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/MIYAGI/Silhouette (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/MIYAGI/Ночь .mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/MIYAGI/Marmalade (ShaHriX Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/MIYAGI/Буревестник (Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/MIYAGI/Не Жалея (Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  MR LAMBO

        elif message.text == "MR LAMBO":
            with open('Remix/Russian/MR LAMBO/Чилим (ShaHriX Remix.mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/MR LAMBO/Shuttle (UNPY REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  NASTY BABE

        elif message.text == "NASTY BABE":
            with open('Remix/Russian/NASTY BABE/По глазам (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  NECHAEV

        elif message.text == "NECHAEV":
            with open('Remix/Russian/NECHAEV/Беги (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  NEEL

        elif message.text == "NEEL":
            with open('Remix/Russian/NEEL/BLACKBERRY (Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/NEEL/Мона Лиза (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  NECOGLAI

        elif message.text == "NEKOGLAI":
            with open('Remix/Russian/NEKOGLAI/Cumback (Arch Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/NEKOGLAI/Cumback (Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  NICENIGHT

        elif message.text == "NICENIGHT":
            with open('Remix/Russian/NICENIGHT/Небо будто вата (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  NIKITATA

        elif message.text == "NIKITATA":
            with open('Remix/Russian/NIKITATA/Спать без тебя (Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  NLO

        elif message.text == "NLO":
            with open('Remix/Russian/NLO/Девочка морока (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/NLO/Плюшевый (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/NLO/Синий джин (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/NLO/Холодный космос (Kxsmic Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  NVRKN134

        elif message.text == "NVRKN134":
            with open('Remix/Russian/NVRKN134/Ты Не Королева (SWERODO Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  NЮ

        elif message.text == "NЮ":
            with open('Remix/Russian/NЮ/NЮ - Никто (BERSKIY Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ODGO

        elif message.text == "ODGO":
            with open('Remix/Russian/ODGO/ТЫ МОЙ ЯД.mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  OXXXYMIRON

        elif message.text == "OXXXYMIRON":
            with open('Remix/Russian/OXXXYMIRON/THE STORY OF ALISHER.mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  PUSSYKILLER

        elif message.text == "PUSSYKILLER":
            with open('Remix/Russian/PUSSYKILLER/Одним выстрелом (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  QYAL QYAL

        elif message.text == "QYAL QYAL":
            with open('Remix/Russian/QYAL QYAL/Мурашки (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  R.RICCADO

        elif message.text == "R.RICCADO":
            with open('Remix/Russian/R.RICCADO/Ну привет (REMIX) .mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/R.RICCADO/Никогда (Karmv Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  RAIKAHO

        elif message.text == "RAIKAHO":
            with open('Remix/Russian/RAIKAHO/Девочка Наркотик (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/RAIKAHO/Подшофе (SWERODO Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  RAKHIM

        elif message.text == "RAKHIM":
            with open('Remix/Russian/RAKHIM/Аккорды (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  RAMIL

        elif message.text == "RAMIL":
            with open('Remix/Russian/RAMIL/Убей Меня (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/RAMIL/Просто лети (Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/RAMIL/MP3 (FriDrix Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/RAMIL/MP3 (ShaHriX Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/RAMIL/Маяк (ShaHriX & FriDrix Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/RAMIL/Не ищи меня (Miki Mouse Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/RAMIL/Убей Меня (Fandi Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/RAMIL/Убей Меня (Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/RAMIL/Увидимся (ShaHriX Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  RASA

        elif message.text == "RASA":
            with open('Remix/Russian/RASA/Фиолетово (UNPY REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/RASA/Offline(REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/RASA/ПОГУДИМ (kxsmic REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  REAL GIRL

        elif message.text == "REAL GIRL":
            with open('Remix/Russian/REAL GIRL/Отпускаю (Cover) (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  SAM WICK

        elif message.text == "SAM WICK":
            with open('Remix/Russian/SAM WICK/Пойми (Subrik Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  SANTY ONE

        elif message.text == "SANTY ONE":
            with open('Remix/Russian/SANTY ONE/Я с тобой (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  SANTIZ

        elif message.text == "SANTIZ":
            with open('Remix/Russian/SANTIZ/Посмотри назад (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  SASHA SANTA

        elif message.text == "SASHA SANTA":
            with open('Remix/Russian/SASHA SANTA/Кавычки (kxsmic remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/SASHA SANTA/18_ (Karmv Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/SASHA SANTA/18_ (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/SASHA SANTA/В душу (Karmv Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  SCIRENA

        elif message.text == "SCIRENA":
            with open('Remix/Russian/SCIRENA/Деньги и Москва (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  SHAMI

        elif message.text == "SHAMI":
            with open('Remix/Russian/SHAMI/Она ищет любовь (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  SHEIKH MANSUR

        elif message.text == "SHEIKH MANSUR":
            with open('Remix/Russian/SHEIKH MANSUR/Балдини (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  SLAVA MARLOW

        elif message.text == "SLAVA MARLOW":
            with open('Remix/Russian/SLAVA MARLOW/Ты далеко (Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  SLAVIK POGOSOV

        elif message.text == "SLAVIK POGOSOV":
            with open('Remix/Russian/SLAVIK POGOSOV/Монро (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/SLAVIK POGOSOV/Монро (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/SLAVIK POGOSOV/Монро.mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  STRANGE

        elif message.text == "STRANGE":
            with open('Remix/Russian/STRANGE/Зависай (BERSKIY Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  STRCTRE

        elif message.text == "STRCTRE":
            with open('Remix/Russian/STRCTRE/Дай огня (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  T1ONE

        elif message.text == "T1ONE":
            with open('Remix/Russian/T1ONE/Вино Помогает (Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  TARAS

        elif message.text == "TARAS":
            with open('Remix/Russian/TARAS/Моя девочка (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  TANIR

        elif message.text == "TANIR":
            with open('Remix/Russian/TANIR/Мама это ночь (Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/TANIR/Аккуратно (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/TANIR/Пуля (karmv remix) (2).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/TANIR/Пуля (KARMV REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  TESLYA

        elif message.text == "TESLYA":
            with open('Remix/Russian/TESLYA/Mercedes (SWERODO Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/TESLYA/Летать (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  TIMRAN

        elif message.text == "TIMRAN":
            with open('Remix/Russian/TIMRAN/Не пускайте танцевать (Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  TINI LIN

        elif message.text == "TINI LIN":
            with open('Remix/Russian/TINI LIN/Последний танец (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    # TORI KVIT

        elif message.text == "TORI KVIT":
            with open('Remix/Russian/TORI KVIT/Девочка (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  V$XV PRINCE

        elif message.text == "V$XV PRINCE":
            with open('Remix/Russian/V$XV PRINCE/Суета (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  VERBEE

        elif message.text == "VERBEE":
            with open('Remix/Russian/VERBEE/Ясный мой свет.mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  VESNA305

        elif message.text == "VESNA305":
            with open('Remix/Russian/VESNA305/Новый год.mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  WELLAY

        elif message.text == "WELLAY":
            with open('Remix/Russian/WELLAY/Танцуй (Remix) (2).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  WHITE GALLOWS

        elif message.text == "WHITE GALLOWS":
            with open('Remix/Russian/WHITE GALLOWS/Призрак.mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/WHITE GALLOWS/Королева бала (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  WHYBABY

        elif message.text == "WHYBABY":
            with open('Remix/Russian/WHYBABY/Paypass (karmv remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  X

        elif message.text == "X":
            with open('Remix/Russian/X/Play.mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  XASSA

        elif message.text == "XASSA":
            with open('Remix/Russian/XASSA/Beautiful Life (Kxsmic & Alexei Shkurko Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/XASSA/Paradise (SWERODO Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/XASSA/Влюбилась в дурака (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/XASSA/Романтик (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  XCHO

        elif message.text == "XCHO":
            with open('Remix/Russian/XCHO/Ты и я (8D REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/XCHO/Вороны (remix) (2).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/XCHO/Вороны (Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/XCHO/Закрыла даль (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/XCHO/Закрыла даль (SWERODO Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/XCHO/Мой мир (Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/XCHO/Про любовь (SWERODO Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/XCHO/Ты и я (Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/XCHO/Где же вы (SLOWED).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  XOLIDAYBOY

        elif message.text == "XOLIDAYBOY":
            with open('Remix/Russian/XOLIDAYBOY/Моя хулиганка (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  YACHEVSKIY

        elif message.text == "YACHEVSKIY":
            with open('Remix/Russian/YACHEVSKIY/BRABUS (BERSKIY REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  YUFOLL

        elif message.text == "YUFOLL":
            with open('Remix/Russian/YUFOLL/В белом платье (Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ZIPPO

        elif message.text == "ZIPPO":
            with open('Remix/Russian/ZIPPO/Остаток слов (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ZOMB

        elif message.text == "ZOMB":
            with open('Remix/Russian/ZOMB/BABY TONIGHT.mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ZOMB/Пантомима (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ZOMB/Селяви (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)










#  RUSSIAN REMIXES (А - Я)  #

    #  АБРИКОСА

        elif message.text == "АБРИКОСА":
            with open('Remix/Russian/АБРИКОСА/Бюджет (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  АДВАЙТА

        elif message.text == "АДВАЙТА":
            with open('Remix/Russian/АДВАЙТА/Ocean (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  АРКАЙДА

        elif message.text == "АРКАЙДА":
            with open('Remix/Russian/АРКАЙДА/С горем да пополам (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/АРКАЙДА/Глупая полюбила.mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/АРКАЙДА/Дай Дыма Брат (ShaHriX Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/АРКАЙДА/Теперь вали (Silver Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  АНДРЕЙ ЛЕНИЦКИЙ

        elif message.text == "АНДРЕЙ ЛЕНИЦКИЙ":
            with open('Remix/Russian/АНДРЕЙ ЛЕНИЦКИЙ/Другой (AdonMix Edit).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  АЛЁНА ШВЕЦ.

        elif message.text == "АЛЁНА ШВЕЦ.":
            with open('Remix/Russian/АЛЁНА ШВЕЦ/Вино_и_Сигареты_Real_Girl_Cover_ShaHriX_Remix.mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  АМУРА

        elif message.text == "АМУРА":
            with open('Remix/Russian/АМУРА/Минимум (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/АМУРА/Спрячься (Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  БОДЯ МИР642

        elif message.text == "БОДЯ МИР642":
            with open('Remix/Russian/БОДЯ МИР642/Meloman (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ВАНЯ ДМИТРЕНКО

        elif message.text == "ВАНЯ ДМИТРЕНКО":
            with open('Remix/Russian/ВАНЯ ДМИТРЕНКО/Лего (Mikis Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ВСЕГДА МЕЧТАЛ

        elif message.text == "ВСЕГДА МЕЧТАЛ":
            with open('Remix/Russian/ВСЕГДАМЕЧТАЛ/Синабон (Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ГАНВЕСТ

        elif message.text == "ГАНВЕСТ":
            with open('Remix/Russian/ГАНВЕСТ/Ты такая GLE (BERSKIY Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ДЕНИС RIDER

        elif message.text == "ДЕНИС RIDER":
            with open('Remix/Russian/ДЕНИС RIDER/Перейдем на ты (kxsmic remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ДЖАЯММИ

        elif message.text == "ДЖАЯММИ":
            with open('Remix/Russian/ДЖАЯММИ/По полям (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ДЖИОС

        elif message.text == "ДЖИОС":
            with open('Remix/Russian/ДЖИОС/Тело (kxsmic remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ДЖИОС/Умотан (KARMV RMX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ЕГОР КРИД

        elif message.text == "ЕГОР КРИД":
            with open('Remix/Russian/ЕГОР КРИД/WE GOTTA GET LOVE (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ЕГОР КРИД/We Gotta Get Love (ShaHriX Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ЕГОР КРИД/Отпускаю (ShaHriX Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ЕГОР КРИД/3-е Сентября (UNPY REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ЕГОР КРИД/3-е Cентября.mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ИНТЕРНАЛ

        elif message.text == "ИНТЕРНАЛ":
            with open('Remix/Russian/ИНТЕРНАЛ/Заболел_ но не тобой (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ИСЛАМ ИТЛЯШЕВ

        elif message.text == "ИСЛАМ ИТЛЯШЕВ":
            with open('Remix/Russian/ИСЛАМ ИТЛЯШЕВ/НА РАХАТЕ (Kxsmic Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  КАНГИ

        elif message.text == "КАНГИ":
            with open('Remix/Russian/КАНГИ/Голова (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/КАНГИ/Голова.mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  КАСПИЙСКИЙ ГРУЗ

        elif message.text == "КАСПИЙСКИЙ ГРУЗ":
            with open('Remix/Russian/КАСПИЙСКИЙ ГРУЗ/На белом (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/КАСПИЙСКИЙ ГРУЗ/18_ (REMIX) (2).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ЛЁША СВИК

        elif message.text == "ЛЁША СВИК":
            with open('Remix/Russian/ЛЁША СВИК/Плакала (Remix) (2).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ЛЁША СВИК/Плакала (Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ЛИВИ

        elif message.text == "ЛИВИ":
            with open('Remix/Russian/ЛИВИ/Влюблён (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ЛЫФАРЬ

        elif message.text == "ЛЫФАРЬ":
            with open('Remix/Russian/ЛЫФАРЬ/Техно (KARMV REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  МАКС КОРЖ

        elif message.text == "МАКС КОРЖ":
            with open('Remix/Russian/МАКС КОРЖ/Не твой (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  МАЛЬБЕК

        elif message.text == "МАЛЬБЕК":
            with open('Remix/Russian/МАЛЬБЕК/Равнодушие (UNPY REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  МИЧЕЛЗ

        elif message.text == "МИЧЕЛЗ":
            with open('Remix/Russian/МИЧЕЛЗ/Она Хочет (kxsmic remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  МОТ

        elif message.text == "МОТ":
            with open('Remix/Russian/МОТ/Август - это ты (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  НИКУБА

        elif message.text == "НИКУБА":
            with open('Remix/Russian/НИКУБА/Мы в порше (Karmv Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ОСТАП ПАРФЁНОВ

        elif message.text == "ОСТАП ПАРФЁНОВ":
            with open('Remix/Russian/ОСТАП ПАРФЁНОВ/Джингл Белс не будет.mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ОСТАП ПАРФЁНОВ/Ты не королева (BERSKIY Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ОСТАП ПАРФЁНОВ/ТЫ НЕ КОРОЛЕВА (Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ПАША PROOROK

        elif message.text == "ПАША PROOROK":
            with open('Remix/Russian/ПАША PROOROK/А любви нашей хана (RENDOW Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ПЛАГА

        elif message.text == "ПЛАГА":
            with open('Remix/Russian/ПЛАГА/Туман.mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ПЛАГА/Раньше (Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ПОШЛЫЙ

        elif message.text == "ПОШЛЫЙ":
            with open('Remix/Russian/ПОШЛЫЙ/Колейдоскоп (Karmv Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  СКРИПТОНИТ

        elif message.text == "СКРИПТОНИТ":
            with open('Remix/Russian/СКРИПТОНИТ/Slow Mo.mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  СУЛТАН ЛАГУЧЕВ

        elif message.text == "СУЛТАН ЛАГУЧЕВ":
            with open('Remix/Russian/СУЛТАН ЛАГУЧЕВ/Не Души (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ТИМА АКИМОВ

        elif message.text == "ТИМА АКИМОВ":
            with open('Remix/Russian/ТИМА АКИМОВ/Пролетело лето.mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ТИМА БЕЛОРУССКИХ

        elif message.text == "ТИМА БЕЛОРУССКИХ":
            with open('Remix/Russian/ТИМА БЕЛОРУССКИХ/Я Больше Не Напишу (Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ТРИ ДНЯ ДОЖДЯ

        elif message.text == "ТРИ ДНЯ ДОЖДЯ":
            with open('Remix/Russian/ТРИ ДНЯ ДОЖДЯ/Я и одиночество (Rendow Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ФЛИТ

        elif message.text == "ФЛИТ":
            with open('Remix/Russian/ФЛИТ/Малиновое небо (karmv Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ФОГЕЛЬ

        elif message.text == "ФОГЕЛЬ":
            with open('Remix/Russian/ФОГЕЛЬ/СТЕРВА (Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ШЕЙХ МАНСУР

        elif message.text == "ШЕЙХ МАНСУР":
            with open('Remix/Russian/ШЕЙХ МАНСУР/Соврал (Karmv & AdonMix Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ЭЛДЖЕЙ

        elif message.text == "ЭЛДЖЕЙ":
            with open('Remix/Russian/ЭЛДЖЕЙ/Harakiri (ShaHriX Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ЭЛДЖЕЙ/Бронежилет (ShaHriX Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ЭНШПИЛЬ

        elif message.text == "ЭНДШПИЛЬ":
            with open('Remix/Russian/ЭНДШПИЛЬ/Туда (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ЭНДШПИЛЬ/Капканы .mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ЭНДШПИЛЬ/Приятная (REMIX).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ЭРИКА ЛУНДМОЕН

        elif message.text == "ЭРИКА ЛУНДМОЕН":
            with open('Remix/Russian/ЭРИКА ЛУНДМОЕН/Яд (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ЮЛИАНА КАРАУЛОВА

        elif message.text == "ЮЛИАНА КАРАУЛОВА":
            with open('Remix/Russian/ЮЛИАНА КАРАУЛОВА/Ты не такой (Kxsmic REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ЮРИЙ ШАТУНОВ

        elif message.text == "ЮРИЙ ШАТУНОВ":
            with open('Remix/Russian/ЮРИЙ ШАТУНОВ/Забудь (SWERODO Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/ЮРИЙ ШАТУНОВ/Седая Ночь (Cvetocek7 Cover) (ShaHriX Remix).mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ЯД ДОБРА

        elif message.text == "ЯД ДОБРА":
            with open('Remix/Russian/ЯД ДОБРА/Банда (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  ЯМЫЧ

        elif message.text == "ЯМЫЧ":
            with open('Remix/Russian/ЯМЫЧ/Чёрный BMW (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  84

        elif message.text == "84":
            with open('Remix/Russian/84/Классная.mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  3-ИЙ ЯНВАРЬ

        elif message.text == "3-ИЙ ЯНВАРЬ":
            with open('Remix/Russian/3-ИЙ ЯНВАРЬ/Переходный возраст (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  5УТРА

        elif message.text == "5УТРА":
            with open('Remix/Russian/5УТРА/Давай сбежим (REMIX).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

            with open('Remix/Russian/5УТРА/Без_тебя_я_тону_в_этом_море_Barabanov_Remix.mp3', 'rb') as remix:
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

    #  100ЛИЦЯ

        elif message.text == "100ЛИЦЯ":
            with open('Remix/Russian/100ЛИЦЯ/Чорнобрива (KARMV Remix).mp3', 'rb') as remix:
                await delete_message_1(message)
                text = await bot.send_message(chat_id = message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
                await asyncio.sleep(0.5)
                await bot.edit_message_text(chat_id = message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
                await bot.send_audio(chat_id = message.chat.id, audio = remix, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
                await bot.delete_message(chat_id = message.chat.id, message_id = text.message_id)

        else:

            await bot.send_message(message.chat.id, "<b> Ничего не нашлось  🙁 </b>", parse_mode = 'html')
            await bot.send_message(message.chat.id, "<b> Убедитесь о правильности имени артиста ❗️ </b>", parse_mode = 'html')
            await bot.delete_message(chat_id = message.chat.id, message_id = message.message_id)










async def send_text(message):
    pass



def send_music(message):
    pass





#  CALLBACK

@dp.callback_query_handler(lambda call: True)
async def callbacks(call: types.CallbackQuery):

#  WEEK 1

    if call.data == "track_11":
        with open("New/Week 1/EGOR_KRID_-_3-e_Sentyabrya_74680760.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_12":
        with open("New/Week 1/VACÍO, MORGENSHTERN - Притон.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_13":
        with open("New/Week 1/kosmonavtov-net-kholodnaja-osen.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_14":
        with open("New/Week 1/GAYAZOV_BROTHER_-_Spasajj_moyu_pyatnicu_74680758.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_15":
        with open("New/Week 1/Blago White - VNATURI.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_16":
        with open("New/Week 1/Tima_Akimov_-_Proletelo_leto_74682968.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_17":
        with open("New/Week 1/The_Limba_-_Ne_bolno_74680759.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_18":
        with open("New/Week 1/PINQ, MAYOT, LOVV66, Scally Milano, uglystephan - Эстакада.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_19":
        with open("New/Week 1/LSP_-_Sektor_Priz_74680800.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_20":
        with open("New/Week 1/rakhim-golden-chain.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

#  WEEK 2

    elif call.data == "track_21":
        with open("New/Week 2/Ваня Дмитренко, Григорий Лепс - Бейби.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_22":
        with open("New/Week 2/Ислам Итляшев - Ресторан.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_23":
        with open("New/Week 2/ELMAN, Andro - Круз.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_24":
        with open("New/Week 2/Люся Чеботина - ПЛАКАЛ ГОЛЛИВУД.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_25":
        with open("New/Week 2/Dabro - Мне не страшно.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_26":
        with open("New/Week 2/Kambulat - Пасмурно.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_27":
        with open("New/Week 2/Oxxxymiron - ОЙДА.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_28":
        with open("New/Week 2/JONY - Никак.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_29":
        with open("New/Week 2/Akmal' - Приснись.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_30":
        with open("New/Week 2/MUJEVA - Чёрный мерседес.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

#  WEEK 3

    elif call.data == "track_31":
        with open("New/Week 3/Элджей & Коста Лакоста - Бронежилет.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_32":
        with open("New/Week 3/Ramil - Просто Лети.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_33":
        with open("New/Week 3/LIZER - Не Герой.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_34":
        with open("New/Week 3/Мари Краймбрери - Не Буди Меня.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_35":
        with open("New/Week 3/Улицы.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_36":
        with open("New/Week 3/Padillion feat. Thomas Mraz - Серебряный Сёрфер.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_37":
        with open("New/Week 3/MAYOT feat. Guf - SUMMERTIME.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_38":
        with open("New/Week 3/МОТ - Любовь как спецэффект.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_39":
        with open("New/Week 3/TONI & Andro - Соври.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_40":
        with open("New/Week 3/Yanix feat. SODA LUV - Badass.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

#  WEEK 4

    elif call.data == "track_41":
        with open("New/Week 4/Ёлка - Заново.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_42":
        with open("New/Week 4/Feduk - Ябеда.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_43":
        with open("New/Week 4/zoloto-neproizoshlo.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_44":
        with open("New/Week 4/Kambulat - Это Любовь.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_45":
        with open("New/Week 4/rydm-city-skriptonit-solo-tu.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_46":
        with open("New/Week 4/Hollyflame - За Твоим Домом.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_47":
        with open("New/Week 4/lali-mukka-budilnik.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_48":
        with open("New/Week 4/Lizer - Дерзко.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_49":
        with open("New/Week 4/Xolidayboy - Моя Хулиганка.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_50":
        with open("New/Week 4/Джизус - Твои Глаза.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

#  WEEK 5

    elif call.data == "track_51":
        with open("New/Week 5/ANNA ASTI - Ночью на кухне.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_52":
        with open("New/Week 5/Три Дня Дождя - Подозрительно.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_53":
        with open("New/Week 5/MACAN - Плачь, но не звони.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_54":
        with open("New/Week 5/Белый Шум, Баста - Белый шум.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_55":
        with open("New/Week 5/kambulat-tyngla-mp3.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_56":
        with open("New/Week 5/Джизус - На Удачу.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_57":
        with open("New/Week 5/DZHARO - Rockstar.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_58":
        with open("New/Week 5/Rakhim, Andro - Разожги во мне огонь.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_59":
        with open("New/Week 5/VACIO - Фотик.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_60":
        with open("New/Week 5/Mr Lambo, Пабло - Авансы.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

#  WEEK 6

    elif call.data == "track_61":
        with open("New/Week 6/Мой Белый.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_62":
        with open("New/Week 6/Смоки Мо feat. Murovei & Guf & Ноггано - OZZY.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_63":
        with open("New/Week 6/Б.О.М.Ж.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_64":
        with open("New/Week 6/Мрак.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_65":
        with open("New/Week 6/Летуаль.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_66":
        with open("New/Week 6/Ты не мечтай даже.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_67":
        with open("New/Week 6/Снова МОТ Стелет.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_68":
        with open("New/Week 6/Пока ты с ним.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_69":
        with open("New/Week 6/Океаны.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_70":
        with open("New/Week 6/Фантазия.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

#  WEEK 7

    elif call.data == "track_71":
        with open("New/Week 7/PHARAOH - Соната ей.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_72":
        with open("New/Week 7/JONY, ANNA ASTI - Как любовь твою понять.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_73":
        with open("New/Week 7/kizaru - Тебя любят там где меня нет.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_74":
        with open("New/Week 7/Баста, Feduk - Времени Нет.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_75":
        with open("New/Week 7/Элджей - Форрест Гамп.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_76":
        with open("New/Week 7/SODA LUV- DTF.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_77":
        with open("New/Week 7/Ольга Серябкина - Эта зима.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_78":
        with open("New/Week 7/104 feat. Hey Monro - Куртка.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_79":
        with open("New/Week 7/Mary Gu, MAYOT - Два выстрела.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_80":
        with open("New/Week 7/ST - Воспоминания.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

#  WEEK 8

    elif call.data == "track_81":
        with open("New/Week 8/104, Скриптонит - BITCH.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_82":
        with open("New/Week 8/10AGE, Шура - Зима.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_83":
        with open("New/Week 8/ANNA ASTI - Звенит январская вьюга.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_84":
        with open("New/Week 8/Konfuz - Скучаю.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_85":
        with open("New/Week 8/Kristina Si - Твой мир.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_86":
        with open("New/Week 8/MAYOT - 4.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_87":
        with open("New/Week 8/OBLADAET - MONSTER TRAKK.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_88":
        with open("New/Week 8/The Limba, JONY, ЕГОР КРИД, А4 - Новогодняя песня.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_89":
        with open("New/Week 8/i61 - SUBMOSCOW SWAG.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_90":
        with open("New/Week 8/Милана Хаметова, DAVA - НОВОГОДНЯЯ.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

#  WEEK 9

    elif call.data == "track_91":
        with open("New/Week 9/Джиган feat. VACÍO, MAYOT - Танцуй со мной.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_92":
        with open("New/Week 9/алёна швец. - Спи.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_93":
        with open("New/Week 9/DZHARO - Cлед.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_94":
        with open("New/Week 9/JABO feat. Konfuz - МНОГО РАЗ.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_95":
        with open("New/Week 9/17 SEVENTEEN - Для тебя и для меня.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_96":
        with open("New/Week 9/Гуф - Про пуделя.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_97":
        with open("New/Week 9/Rakhim - Look At Me Habibi.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_98":
        with open("New/Week 9/Эллаи - Набери.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_99":
        with open("New/Week 9/UBEL - Никогда-нибудь.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_100":
        with open("New/Week 9/Idris & Leos - Первой не пиши.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

#  WEEK 10

    elif call.data == "track_101":
        with open("New/Week 10/GUMA, КУОК - Притяжение.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_102":
        with open("New/Week 10/Элджей - Изиранеры.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_103":
        with open("New/Week 10/HammAli & Navai - Засыпай Красавица.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_104":
        with open("New/Week 10/Mr Lambo, Xcho - Roles.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_105":
        with open("New/Week 10/Егор Натс feat. М - ВЫДОХНИ.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_106":
        with open("New/Week 10/Basiaga - Валим.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_107":
        with open("New/Week 10/Dabro - Надо повторить.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_108":
        with open("New/Week 10/Andro - Дай Мне Только Шанс.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_109":
        with open("New/Week 10/Boulevard_Depo_Da.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_110":
        with open("New/Week 10/Люся Чеботина - ProОзеро.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

#  WEEK 11

    elif call.data == "track_111":
        with open("New/Week 11/Miyagi & Эндшпиль - По полям.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_112":
        with open("New/Week 11/Konfuz - Тише.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_113":
        with open("New/Week 11/HammAli & Navai - Ноты.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_114":
        with open("New/Week 11/MONA, Баста - Ты так мне необходим.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_115":
        with open("New/Week 11/Armich - Смесь.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_116":
        with open("New/Week 11/blago white, LOVV66, Молодой Платон - Выше.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_117":
        with open("New/Week 11/KARA KROSS, MANIL - Чёртово колесо.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_118":
        with open("New/Week 11/Sqwore - Детство.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_119":
        with open("New/Week 11/Три Дня Дождя - За Край.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_120":
        with open("New/Week 11/луни ана - DO U CALL ME.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

#  WEEK 12

    elif call.data == "track_121":
        with open("New/Week 12/Кравц & Гио ПиКа - Где прошла ты.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_122":
        with open("New/Week 12/kizaru - Зеркало.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_123":
        with open("New/Week 12/Jakone & SCIRENA - По Весне.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_124":
        with open("New/Week 12/MACAN feat. SCIRENA - IVL.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_125":
        with open("New/Week 12/MACAN - ASPHALT 8.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_126":
        with open("New/Week 12/Pepel Nahudi - Заново завоевать.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_127":
        with open("New/Week 12/A.V.G feat. Goro - Она Близко.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_128":
        with open("New/Week 12/NLO - Танцы.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_129":
        with open("New/Week 12/SOSKA 69 - Чёрная машина.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_130":
        with open("New/Week 12/ANNA ASTI - Верю в тебя.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

#  WEEK 13

    elif call.data == "track_131":
        with open("New/Week 13/Markul feat. FEDUK - Мятный.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_132":
        with open("New/Week 13/Wildways feat. Mary Gu - Я Тебя Тоже.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_133":
        with open("New/Week 13/Ваня Дмитриенко feat. Моя Мишель - Рыбка.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_134":
        with open("New/Week 13/ЕГОР НАТС - ОЧЕНЬ СКУЧАЮ.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_135":
        with open("New/Week 13/Канги - Ой.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_136":
        with open("New/Week 13/NЮ - Улыбашка.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_137":
        with open("New/Week 13/ЧИНА - ДЕРЗКАЯ.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_138":
        with open("New/Week 13/Kambulat - Марокканка.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_139":
        with open("New/Week 13/GUMA feat. Dyce - Бронежилет.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_140":
        with open("New/Week 13/Артур Пирожков - Позитив.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

#  WEEK 14

    elif call.data == "track_141":
        with open("New/Week 14/ANNA ASTI - Царица.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_142":
        with open("New/Week 14/Miyagi & Эндшпиль - Bounty.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_143":
        with open("New/Week 14/Ислам Итляшев - Довела.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_144":
        with open("New/Week 14/MACAN - Самый пьяный округ в мире.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_145":
        with open("New/Week 14/MAYOT - Мотылёк.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_146":
        with open("New/Week 14/Баста - Девочка-Самурай.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_147":
        with open("New/Week 14/NLO - Молодость Для Тус.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_148":
        with open("New/Week 14/XOLIDAYBOY - Малышка хочет движа.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_149":
        with open("New/Week 14/МУККА - Бурями.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_150":
        with open("New/Week 14/Xcho - Музыка В Ночи.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

#  WEEK 15

    elif call.data == "track_151":
        with open("New/Week 15/MACAN, Jakone - Поспешили.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_152":
        with open("New/Week 15/A.V.G - Я Плачу.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_153":
        with open("New/Week 15/Винтаж, ТРАВМА,SKIDRI, DVRKLXGHT - Плохая Девочка.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_154":
        with open("New/Week 15/Konfuz,The Limba - Ты и Я.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_155":
        with open("New/Week 15/ANNA ASTI - Царица.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_156":
        with open("New/Week 15/Niletto - Летний Дождь.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_157":
        with open("New/Week 15/MONA - Верю в любовь.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_158":
        with open("New/Week 15/VERBEE - Обнимай.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_159":
        with open("New/Week 15/Goro - Во мне столько любви.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_160":
        with open("New/Week 15/A.V.G feat. Goro - Она Близко.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

#  WEEK 16

    elif call.data == "track_161":
        with open("New/Week 16/ANNA ASTI - Дурак.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_162":
        with open("New/Week 16/AUGUST feat. MAYOT - Every Day.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_163":
        with open("New/Week 16/Aarne, uglystephan - Клянусь.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_164":
        with open("New/Week 16/DZHARO - Бесконечность.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_165":
        with open("New/Week 16/Heronwater - 2 часа ночи.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_166":
        with open("New/Week 16/Kamazz feat. NLO - Большие Города.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_167":
        with open("New/Week 16/Levandowskiy, Гио Пика - Вена-Париж.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_168":
        with open("New/Week 16/Niletto & Goshu - Ты Чё Такая Смелая_.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_169":
        with open("New/Week 16/ПАБЛО & Mr Lambo - Чилим.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_170":
        with open("New/Week 16/Тима Акимов - Точно да.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

#  WEEK 17

    elif call.data == "track_171":
        with open("New/Week 17/Aarne feat. Big Baby Tape & Toxi$ & Chief Keef - 4 ur girl.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_172":
        with open("New/Week 17/CHEBANOV feat. Асия - Огни Москвы.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_173":
        with open("New/Week 17/Guf feat. A.V.G - Спонсор Твоих Проблем.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_174":
        with open("New/Week 17/HENSY - Монолог.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_175":
        with open("New/Week 17/OBLADAET - Britney.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_176":
        with open("New/Week 17/Ramil', MACAN - Не играй в любовь.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_177":
        with open("New/Week 17/Zivert - НАД КРЫШАМИ.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_178":
        with open("New/Week 17/Алёна Швец. - Обидно.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_179":
        with open("New/Week 17/Люся Чеботина - ПСЕВДОМОДЕЛИ.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)

    elif call.data == "track_180":
        with open("New/Week 17/Тима Акимов - Космонавт.mp3", "rb") as track:
            text = await bot.send_message(chat_id = call.message.chat.id, text = '<b> Отправляется . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . </b>', parse_mode = 'html')
            await asyncio.sleep(0.5)
            await bot.edit_message_text(chat_id = call.message.chat.id, message_id = text.message_id, text = '<b> Отправляется . . . </b>', parse_mode = 'html')
            await bot.send_audio(chat_id = call.message.chat.id, audio = track, caption = '<a href = "http://t.me/XITMusicx_Bot"> 🔍 Нажми чтобы найти треки </a>', parse_mode = 'html')
            await bot.delete_message(chat_id = call.message.chat.id, message_id = text.message_id)



#  NEXT CALLBACKS

    elif call.data == "next_week_16":
        await bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "<b> Новинки октября: </b>", parse_mode = "html", reply_markup = inline_markups.week_16)
        await bot.answer_callback_query(callback_query_id = call.id, show_alert = False, text = "Новинки октября:")

    elif call.data == "next_week_15":
        await bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "<b> Новинки сентября: </b>", parse_mode = "html", reply_markup = inline_markups.week_15)
        await bot.answer_callback_query(callback_query_id = call.id, show_alert = False, text = "Новинки сентября:")

    elif call.data == "next_week_14":
        await bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "<b> Новинки июля: </b>", parse_mode = "html", reply_markup = inline_markups.week_14)
        await bot.answer_callback_query(callback_query_id = call.id, show_alert = False, text = "Новинки июля:")

    elif call.data == "next_week_13":
        await bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "<b> Новинки июня: </b>", parse_mode = "html", reply_markup = inline_markups.week_13)
        await bot.answer_callback_query(callback_query_id = call.id, show_alert = False, text = "Новинки июня:")

    elif call.data == "next_week_12":
        await bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "<b> Новинки мая: </b>", parse_mode = "html", reply_markup = inline_markups.week_12)
        await bot.answer_callback_query(callback_query_id = call.id, show_alert = False, text = "Новинки мая:")

    elif call.data == "next_week_11":
        await bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "<b> Новинки апреля: </b>", parse_mode = "html", reply_markup = inline_markups.week_11)
        await bot.answer_callback_query(callback_query_id = call.id, show_alert = False, text = "Новинки апреля:")

    elif call.data == "next_week_10":
        await bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "<b> Новинки марта: </b>", parse_mode = "html", reply_markup = inline_markups.week_10)
        await bot.answer_callback_query(callback_query_id = call.id, show_alert = False, text = "Новинки марта:")

    elif call.data == "next_week_9":
        await bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "<b> Новинки января: </b>", parse_mode = "html", reply_markup = inline_markups.week_9)
        await bot.answer_callback_query(callback_query_id = call.id, show_alert = False, text = "Новинки января:")

    elif call.data == "next_week_8":
        await bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "<b> Новинки декабря: </b>", parse_mode = "html", reply_markup = inline_markups.week_8)
        await bot.answer_callback_query(callback_query_id = call.id, show_alert = False, text = "Новинки декабря:")

    elif call.data == "next_week_7":
        await bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "<b> Новинки декабря: </b>", parse_mode = "html", reply_markup = inline_markups.week_7)
        await bot.answer_callback_query(callback_query_id = call.id, show_alert = False, text = "Новинки декабря:")

    elif call.data == "next_week_6":
        await bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "<b> Новинки ноября: </b>", parse_mode = "html", reply_markup = inline_markups.week_6)
        await bot.answer_callback_query(callback_query_id = call.id, show_alert = False, text = "Новинки ноября:")

    elif call.data == "next_week_5":
        await bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "<b> Новинки октября: </b>", parse_mode = "html", reply_markup = inline_markups.week_5)
        await bot.answer_callback_query(callback_query_id = call.id, show_alert = False, text = "Новинки октября:")

    elif call.data == "next_week_4":
        await bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "<b> Новинки октября: </b>", parse_mode = "html", reply_markup = inline_markups.week_4)
        await bot.answer_callback_query(callback_query_id = call.id, show_alert = False, text = "Новинки октября:")

    elif call.data == "next_week_3":
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="<b> Новинки сентября: </b>", parse_mode="html", reply_markup=inline_markups.week_3)
        await bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Новинки сентября:")

    elif call.data == "next_week_2":
        await bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "<b> Новинки сентября: </b>", parse_mode = "html", reply_markup = inline_markups.week_2)
        await bot.answer_callback_query(callback_query_id = call.id, show_alert = False, text = "Новинки сентября:")

    elif call.data == "next_week_1":
        await bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.message_id, text = "<b> Новинки августа: </b>", parse_mode = "html", reply_markup = inline_markups.week_1)
        await bot.answer_callback_query(callback_query_id = call.id, show_alert = False, text = "Новинки августа:")

#  BACK CALLBACKS

    elif call.data == "back_week_17":
        await bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "<b> Топ 10 новинок этой недели: </b>", parse_mode = "html", reply_markup = inline_markups.week_17)
        await bot.answer_callback_query(callback_query_id = call.id, show_alert = False, text = "Топ 10 новинок этой недели:")

    elif call.data == "back_week_16":
        await bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "<b> Новинки октября: </b>", parse_mode = "html", reply_markup = inline_markups.week_16)
        await bot.answer_callback_query(callback_query_id = call.id, show_alert = False, text = "Новинки октября:")

    elif call.data == "back_week_15":
        await bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "<b> Новинки сентября: </b>", parse_mode = "html", reply_markup = inline_markups.week_15)
        await bot.answer_callback_query(callback_query_id = call.id, show_alert = False, text = "Новинки сентября:")

    elif call.data == "back_week_14":
        await bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "<b> Новинки июля: </b>", parse_mode = "html", reply_markup = inline_markups.week_14)
        await bot.answer_callback_query(callback_query_id = call.id, show_alert = False, text = "Новинки июля:")

    elif call.data == "back_week_13":
        await bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "<b> Новинки июня: </b>", parse_mode = "html", reply_markup = inline_markups.week_13)
        await bot.answer_callback_query(callback_query_id = call.id, show_alert = False, text = "Новинки июня:")

    elif call.data == "back_week_12":
        await bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "<b> Новинки мая: </b>", parse_mode = "html", reply_markup = inline_markups.week_12)
        await bot.answer_callback_query(callback_query_id = call.id, show_alert = False, text = "Новинки мая:")

    elif call.data == "back_week_11":
        await bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "<b> Новинки апреля: </b>", parse_mode = "html", reply_markup = inline_markups.week_11)
        await bot.answer_callback_query(callback_query_id = call.id, show_alert = False, text = "Новинки апреля:")

    elif call.data == "back_week_10":
        await bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "<b> Новинки марта: </b>", parse_mode = "html", reply_markup = inline_markups.week_10)
        await bot.answer_callback_query(callback_query_id = call.id, show_alert = False, text = "Новинки марта:")

    elif call.data == "back_week_9":
        await bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.message_id, text = "<b> Новинки января </b>", parse_mode = "html", reply_markup = inline_markups.week_9)
        await bot.answer_callback_query(callback_query_id = call.id, show_alert=False, text = "Новинки января")

    elif call.data == "back_week_8":
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id = call.message.message_id, text = "<b> Новинки декабря: </b>", parse_mode = "html", reply_markup = inline_markups.week_8)
        await bot.answer_callback_query(callback_query_id = call.id, show_alert = False, text = "Новинки декабря:")

    elif call.data == "back_week_7":
        await bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "<b> Новинки декабря: </b>", parse_mode = "html", reply_markup = inline_markups.week_7)
        await bot.answer_callback_query(callback_query_id = call.id, show_alert = False, text = "Новинки декабря:")

    elif call.data == "back_week_6":
        await bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "<b> Новинки ноября: </b>", parse_mode = "html", reply_markup = inline_markups.week_6)
        await bot.answer_callback_query(callback_query_id = call.id, show_alert = False, text = "Новинки ноября:")

    elif call.data == "back_week_5":
        await bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "<b> Новинки октября: </b>", parse_mode = "html", reply_markup = inline_markups.week_5)
        await bot.answer_callback_query(callback_query_id = call.id, show_alert = False, text = "Новинки октября:")

    elif call.data == "back_week_4":
        await bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "<b> Новинки октября: </b>", parse_mode = "html", reply_markup = inline_markups.week_4)
        await bot.answer_callback_query(callback_query_id = call.id, show_alert = False, text = "Новинки октября:")

    elif call.data == "back_week_3":
        await bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "<b> Новинки сентября: </b>", parse_mode = "html", reply_markup = inline_markups.week_3)
        await bot.answer_callback_query(callback_query_id = call.id, show_alert = False, text = "Новинки сентября:")

    elif call.data == "back_week_2":
        await bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "<b> Новинки сентября: </b>", parse_mode = "html", reply_markup = inline_markups.week_2)
        await bot.answer_callback_query(callback_query_id = call.id, show_alert = False, text = "Новинки сентября:")



#  CHECK SUBSCRIBE

    elif call.data == "check":
        await bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
        await check_subscribe(call)





#  CHECK SUNSCRIPTION

async def check_subscribe(call):
    user = call.from_user
    firstname = user.first_name
    lastname = user.last_name
    username = user.username

    sql.execute(f'SELECT id FROM user_data WHERE id = ?' , (call.message.chat.id,))
    user_id = sql.fetchone()

    if user_id is None:
        if await check_subscribtions(config.CHANNELS, call.message.chat.id):
            await bot.send_message(call.message.chat.id, '<b> Добро пожаловать 👋 </b>', parse_mode='html', reply_markup = reply_markups.menu_reply)
            sql.execute('INSERT INTO user_data (id, username, firstname, lastname) VALUES (?, ?, ?, ?)',
            (call.message.chat.id, username, firstname, lastname))
            db.commit()
        else:
            await bot.send_message(call.message.chat.id, '<b> Чтобы пользоваться ботом, подпишитесь на наши каналы ❗️ </b>', parse_mode = 'html', reply_markup = inline_markups.subscribe_inline)
    else:
        if await check_subscribtions(config.CHANNELS, call.message.chat.id):
            await bot.send_message(call.message.chat.id, '<b> Добро пожаловать 👋 </b>', parse_mode='html', reply_markup = reply_markups.menu_reply)
        else:
            await bot.send_message(call.message.chat.id, '<b> Чтобы пользоваться ботом, подпишитесь на наши каналы ❗️ </b>', parse_mode = 'html', reply_markup = inline_markups.subscribe_inline)



#  DELETE MESSAGE 1
async def delete_message_1(message):
    try:
        await bot.delete_message(chat_id = message.chat.id, message_id = message.message_id)
    except:
        pass

#  DELETE MESSAGE 2
async def delete_message_2(message):
    try:
        await bot.delete_message(chat_id = message.chat.id, message_id = message.message_id)
        await bot.delete_message(chat_id = message.chat.id, message_id = message.message_id - 1)
    except:
        pass

#  DELETE MESSAGE 3
async def delete_message_3(message):
    try:
        await bot.delete_message(chat_id = message.chat.id, message_id = message.message_id)
        await bot.delete_message(chat_id = message.chat.id, message_id = message.message_id - 1)
        await bot.delete_message(chat_id = message.chat.id, message_id = message.message_id - 2)
    except:
        pass





#  ON START UP
async def start_bot(_):
    sql.execute('SELECT COUNT(id) FROM user_data')
    all_users = sql.fetchone()[0]

    await bot.send_message(284929331, 'Бот успешно перезапущен !')
    await bot.send_message(284929331, f'Количество пользователей:  <b>{all_users}</b>', parse_mode = 'html')
    # await bot.send_message(1020303972, 'Бот успешно перезапущен !')
    # await bot.send_message(1020303972, f'Количество пользователей:  <b>{all_users}</b>', parse_mode = 'html')




#  LAUNCH
if __name__ == '__main__':
    try:
        executor.start_polling(dp, skip_updates = True, on_startup = start_bot)
    except Exception as e:
        print(e)