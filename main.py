import os
import telebot
import logging
import psycopg2
from config import *
from flask import Flask, request
from telebot import types
import random

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
    dist = 'Привет, бот на стадии разработки...'

    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    button2 = types.KeyboardButton(text="ℹ️Test")
    button1 = types.KeyboardButton(text="⚙️ Options")
    keyboard.add(button2, button1)

    bot.send_photo(message.from_user.id, photo , dist, reply_markup=keyboard)


    db_object.execute(f"SELECT id FROM users WHERE id = {user_id}")
    result = db_object.fetchone()

    if not result:
        if username == None:
            db_object.execute("INSERT INTO users(id, username, messages, firstname) VALUES (%s, %s, %s, %s)",
                              (user_id, "None", 0, userfirst))
            db_connection.commit()
        else:
            db_object.execute("INSERT INTO users(id, username, messages, firstname) VALUES (%s, %s, %s, %s)",
                              (user_id, username, 0, userfirst))
            db_connection.commit()

    update_messages_count(user_id)




@bot.message_handler(commands=["stats"])
def get_stats(message):
    db_object.execute("SELECT * FROM users ORDER BY messages DESC LIMIT 10")
    result = db_object.fetchall()

    if not result:
        bot.reply_to(message, "No data...")
    else:
            reply_message = "Топ 10 спамеров:\n"
            for i, item in enumerate(result):
                reply_message += f"{i + 1}. {item[3].strip()}: {item[2]} смс\n"
            bot.reply_to(message, reply_message)

    update_messages_count(message.from_user.id)


@bot.message_handler(commands=["info"])
def get_stats(message):
    db_object.execute(f"SELECT * FROM users WHERE id = {802515951}")
    result = db_object.fetchall()
    if not result:
        bot.reply_to(message, "No data...")
    else:
            for item in enumerate(result):
                bot.send_message(message.from_user.id, f"{item[0]}, {item[3]}")

    update_messages_count(message.from_user.id)


@bot.message_handler(func=lambda message: True, content_types=["text"])
def message_from_user(message):
    user_id = message.from_user.id
    update_messages_count(user_id)


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

