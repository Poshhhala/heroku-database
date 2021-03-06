import os
import telebot
import logging
import psycopg2
from config import *
from flask import Flask, request
from telebot import types
import random

Photobybot2 = -387904708
Chanal = -1001270568536
admin = 802515951
UrlChanal = 'https://t.me/paparaccii'

bot = telebot.TeleBot(BOT_TOKEN)
server = Flask(__name__)
logger = telebot.logger
logger.setLevel(logging.DEBUG)

db_connection = psycopg2.connect(DB_URI, sslmode="require")
db_object = db_connection.cursor()


def update_messages_count(user_id):
    db_object.execute(f"UPDATE users SET messages = messages + 1 WHERE id = {user_id}")
    db_connection.commit()


@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    userfirst = message.from_user.first_name
    username = message.from_user.username
    photo = 'https://vk.com/deluxe_in_mainstream?z=photo-58122416_457239128%2Falbum-58122416_00%2Frev'
    dist = '*Привет, бот на стадии разработки...\n\nДля предотвращения ошибок рекомендую прочитать\n‼предупреждение*'

    keyboard = telebot.types.ReplyKeyboardMarkup(True)

    button1 = types.KeyboardButton(text="ℹ️Test")
    button2 = types.KeyboardButton(text="👤 Profile")
    button3 = types.KeyboardButton(text="‼️Warning ‼️")


    keyboard.add(button1,button2)
    keyboard.add(button3)

    bot.send_photo(message.from_user.id, photo , dist, reply_markup=keyboard, parse_mode='Markdown')

    db_object.execute(f"SELECT id FROM users WHERE id = {user_id}")
    result = db_object.fetchone()

    # Добавляем в базу
    if not result: # Если нет в базе
        if username == None:
            db_object.execute("INSERT INTO users(id, username, messages, firstname) VALUES (%s, %s, %s, %s)",
                              (user_id, "None", 0, userfirst))
            db_connection.commit()
        else:
            db_object.execute("INSERT INTO users(id, username, messages, firstname) VALUES (%s, %s, %s, %s)",
                              (user_id, username, 0, userfirst))
            db_connection.commit()
    # если есть
    update_messages_count(user_id)
    db_connection.commit()

@bot.callback_query_handler(func=lambda call: True)
def iqchery(call):
        if call.message:
            id = call.message.caption
            db_object.execute("SELECT * FROM users WHERE id = {0}".format(id))
            result = db_object.fetchall()
            db_connection.commit()
            if not result:
                bot.reply_to(call.message, "No data...")
            else:
                for item in result:
                        caption_os = f"*𝔭𝔞𝔭𝔞𝔯𝔞𝔠𝔦 🧛🏻 : {item[3]}*"
                        caption_ok = f"*posted - by: {item[3]}*"

                        linktogroup = types.InlineKeyboardMarkup()

                        linktogroup1 = types.InlineKeyboardButton(text='Поделиться своим контентом 🌉', url='https://t.me/chupadesubot')
                        linktogroup2 = types.InlineKeyboardButton(text='Поделиться своим контентом 🌄', url='https://t.me/chupadesubot')
                        linktogroup3 = types.InlineKeyboardButton(text='Поделиться своим контентом 🌅', url='https://t.me/chupadesubot')
                        linktogroup4 = types.InlineKeyboardButton(text='Поделиться своим контентом 🎆', url='https://t.me/chupadesubot')
                        linktogroup5 = types.InlineKeyboardButton(text='Поделиться своим контентом 🌇', url='https://t.me/chupadesubot')

                        linktogroup.add(random.choice([linktogroup1, linktogroup2, linktogroup3, linktogroup4,linktogroup5]))


                        if call.data == '999':  # by people
                            db_object.execute(f"UPDATE users SET add = add + 1 WHERE id = {call.message.caption}")
                            idphoto = call.message.photo[0].file_id
                            bot.send_photo(Chanal, idphoto, caption_os, parse_mode='Markdown')
                            bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=caption_ok, parse_mode='Markdown')
                            db_connection.commit()

                        if call.data == '998':  # by people
                            db_object.execute(f"UPDATE users SET add = add + 1 WHERE id = {call.message.caption}")
                            idvideo = call.message.video.file_id
                            bot.send_video(Chanal, idvideo, None, caption_os, parse_mode='Markdown')
                            bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=caption_ok, parse_mode='Markdown')
                            db_connection.commit()

                        if call.data == '997':  # by people
                            db_object.execute(f"UPDATE users SET add = add + 1 WHERE id = {call.message.caption}")
                            idmusic = call.message.audio.file_id
                            bot.send_audio(Chanal, idmusic, caption_os, parse_mode='Markdown')
                            bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=caption_ok, parse_mode='Markdown')
                            db_connection.commit()

                        if call.data == '100016781':  # by people + link
                            db_object.execute(f"UPDATE users SET add = add + 1 WHERE id = {call.message.caption}")
                            idphoto = call.message.photo[0].file_id
                            bot.send_photo(Chanal, idphoto, caption_os, reply_markup=linktogroup,parse_mode='Markdown')
                            bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=caption_ok, parse_mode='Markdown')
                            db_connection.commit()

                        if call.data == '100016783':  # by people + link
                            db_object.execute(f"UPDATE users SET add = add + 1 WHERE id = {call.message.caption}")
                            idvideo = call.message.video.file_id
                            bot.send_video(Chanal, idvideo, None, caption_os, reply_markup=linktogroup,parse_mode='Markdown')
                            bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=caption_ok, parse_mode='Markdown')
                            db_connection.commit()

                        if call.data == '100016785':  # by people + link
                            db_object.execute(f"UPDATE users SET add = add + 1 WHERE id = {call.message.caption}")
                            idmusic = call.message.audio.file_id
                            bot.send_audio(Chanal, idmusic, caption_os, reply_markup=linktogroup, parse_mode='Markdown')
                            bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=caption_ok, parse_mode='Markdown')
                            db_connection.commit()

                db_connection.commit()



@bot.message_handler(content_types=['text'])
def handle_text(message):
        if message.text == "◀️ Exit":

            keyboard = telebot.types.ReplyKeyboardMarkup(True)

            button1 = types.KeyboardButton(text="ℹ️Test")
            button2 = types.KeyboardButton(text="👤 Profile")


            keyboard.add(button1, button2)

            bot.reply_to(message, "*Вернул в основное меню !*", reply_markup=keyboard, parse_mode='Markdown')
            db_connection.commit()
        elif message.text == "ℹ️Test":
            bot.reply_to(message, "*Бот активен...\n*", parse_mode='Markdown')
            db_connection.commit()

        elif message.text == "‼️Warning ‼️":
            caption = "*Привет, спасибо что начал(а) читать...\n\nБот разложеный на бесплатном сервисе и я не знаю как он будет себя вести.\n\nПеред началом взаимодействий с ботом - прожми ТЕСТ и потожди пока он ответит (он может отправить сразу 2 смс в ответ, это норма), дальше можешь делать свои дела.\n\nОбнял - поцеловал 🫶🏻*"
            bot.reply_to(message, caption, parse_mode='Markdown')

        elif message.text == "👤 Profile":

                id = message.from_user.id
                db_object.execute("SELECT * FROM users WHERE id = {0}".format(id))
                result = db_object.fetchall()
                if not result:
                    bot.reply_to(message, "No data...")
                else:
                    for item in result:

                        caption = f"*📊 Твоя личная информация\n➖➖➖➖➖\n👤 {item[3]}👥 @{item[1]}⬆️ Информация может быть устарелой\n➖➖➖➖➖\nОтправлено боту:\n🌄 Фотографии: {item[4]}\n📹 Видео: {item[5]}\n🎵 Музыка: {item[6]}\n➖➖➖➖➖\n✅ Всего одобрено в группу: {item[7]}*"
                        bot.send_message(message.chat.id, caption, parse_mode='Markdown')
                update_messages_count(message.from_user.id)
                db_connection.commit()
        else:
                cap = random.choice([('*📹 Отправь мне видео...*'),('*🌄 Жду фотографии...*'), ('*🎵 Скинь свой любимый трек*')])
                bot.delete_message(message.chat.id, message.message_id)
                bot.send_message(message.chat.id, cap, parse_mode='Markdown')


# @bot.message_handler(commands=["stats"])
# def get_stats(message):
#     db_object.execute("SELECT * FROM users ORDER BY messages DESC LIMIT 10")
#     result = db_object.fetchall()
#
#     if not result:
#         bot.reply_to(message, "No data...")
#     else:
#             reply_message = "Топ 10 спамеров:\n"
#             for i, item in enumerate(result):
#                 reply_message += f"{i + 1}. {item[3].strip()}: {item[2]} смс\n"
#             bot.reply_to(message, reply_message)
#
#     update_messages_count(message.from_user.id)

@bot.message_handler(content_types=["photo"])
def photo(message):
                button = telebot.types.InlineKeyboardMarkup()
                button1 = types.InlineKeyboardButton(text="✅ - Post", callback_data=999)
                button.add(button1)

                caption = "{0}".format(message.from_user.id)

                idphoto = message.photo[0].file_id
                user_id = message.from_user.id
                db_object.execute(f"UPDATE users SET photo = photo + 1 WHERE id = {user_id}")

                bot.reply_to(message, random.choice(["*✅ - Миссия выполнена, продолжай!*",
                                                 "*✅ - Хорошая работа, Олег!*",
                                                 "*✅ - Я кончаю, продолжай!*",
                                                 "*✅ - Хочу ещё!*", "*✅ - Я уже тебя люблю!*",
                                                 "*✅ - Ты меня обрадовал :3!*",
                                                 "*✅ - Иди поцелую!!*",
                                                 "*✅ - Жди! Может опубликую в канале!*",
                                                 "*✅ - Красиво!*",
                                                 "*✅ - Спасибо, Бро!*",
                                                 "*✅ - Прекрасно!*", ]), parse_mode='Markdown')
                bot.send_photo(Photobybot2, idphoto, caption, reply_markup=button, parse_mode='Markdown')
                db_connection.commit()


@bot.message_handler(content_types=["video"])
def video(message):
            button = telebot.types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton(text="✅ - Post", callback_data=998)
            button.add(button1)

            idvideo = message.video.file_id
            user_id = message.from_user.id
            db_object.execute(f"UPDATE users SET video = video + 1 WHERE id = {user_id}")
            caption = "{0}".format(message.from_user.id)

            bot.reply_to(message, random.choice(["*✅ - Миссия выполнена, продолжай!*",
                                             "*✅ - Хорошая работа, Олег!*",
                                             "*✅ - Я кончаю, продолжай!*",
                                             "*✅ - Хочу ещё!*", "*✅ - Я уже тебя люблю!*",
                                             "*✅ - Ты меня обрадовал :3!*",
                                             "*✅ - Иди поцелую!!*",
                                             "*✅ - Жди! Может опубликую в канале!*",
                                             "*✅ - Красиво!*",
                                             "*✅ - Спасибо, Бро!*",
                                             "*✅ - Прекрасно!*", ]), parse_mode='Markdown')
            bot.send_video(Photobybot2, idvideo, None, caption, reply_markup=button, parse_mode='Markdown')
            db_connection.commit()

@bot.message_handler(content_types=["audio"])
def audio(message):
            button = telebot.types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton(text="✅ - Post", callback_data=997)
            button.add(button1)

            caption = "{0}".format(message.from_user.id)

            idmusic = message.audio.file_id
            user_id = message.from_user.id
            db_object.execute(f"UPDATE users SET music = music + 1 WHERE id = {user_id}")
            bot.reply_to(message, random.choice(["*✅ - Миссия выполнена, продолжай!*",
                                             "*✅ - Хорошая работа, Олег!*",
                                             "*✅ - Я кончаю, продолжай!*",
                                             "*✅ - Хочу ещё!*", "*✅ - Я уже тебя люблю!*",
                                             "*✅ - Ты меня обрадовал :3!*",
                                             "*✅ - Иди поцелую!!*",
                                             "*✅ - Жди! Может опубликую в канале!*",
                                             "*✅ - Красиво!*",
                                             "*✅ - Спасибо, Бро!*",
                                             "*✅ - Прекрасно!*", ]), parse_mode='Markdown')
            bot.send_audio(Photobybot2, idmusic, caption, reply_markup=button, parse_mode='Markdown')
            db_connection.commit()


@server.route(f"/{BOT_TOKEN}", methods=["POST"])
def redirect_message():
    json_string = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL)
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 4999)))