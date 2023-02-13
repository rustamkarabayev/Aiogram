from googletrans import Translator

import aiogram
import config as cfg
import keyboard as k
from aiogram import types
import sqlite3
transl = Translator()

bot = aiogram.Bot(token=cfg.TOKEN)
dp = aiogram.Dispatcher(bot)
con = sqlite3.connect('translator.db')


@dp.message_handler(commands=['start'])
async def start(message: aiogram.types.Message):
    mycursor = con.cursor()
    sql = "SELECT * FROM users WHERE id = ?"
    adr = (str(message.from_user.id),)
    mycursor.execute(sql, adr)
    myresult = mycursor.fetchall()
    print(myresult)
    if myresult is None or myresult == [] or myresult == ():
        mycursor = con.cursor()
        sql = "INSERT INTO users (id, language) VALUES (?, ?)"
        val = (str(message.from_user.id), "ru")
        mycursor.execute(sql, val)
        con.commit()
        await message.reply("Зарегестрирован!")
    await message.reply(cfg.STARTMESSAGE)


@dp.message_handler(commands=['choose'])
async def starting(message: aiogram.types.Message):
    await message.reply(cfg.CHOOSEMESSAGE, reply_markup=k.keyb)


@dp.callback_query_handler(lambda c: c.data)
async def process_callback_kb1btn1(callback_query: aiogram.types.CallbackQuery):
    if callback_query.data in cfg.LANGUES:
        lang = callback_query.data
        mycursor = con.cursor()
        sql = "UPDATE users SET language = ? WHERE id = ?"
        val = (lang, str(callback_query.from_user.id))
        mycursor.execute(sql, val)
        await bot.send_message(callback_query.from_user.id, "Язык изменен на " + cfg.LANGDICT[lang])


@dp.message_handler()
async def echo_message(msg: types.Message):
    mycursor = con.cursor()
    sql = "SELECT * FROM users WHERE id = ?"
    adr = (msg.from_user.id,)
    mycursor.execute(sql, adr)
    myresult = mycursor.fetchall()
    language = myresult[0][1]
    word = transl.translate(msg.text, dest=language).text
    await bot.send_message(msg.from_user.id, word)

if __name__ == '__main__':
    aiogram.executor.start_polling(dp)
