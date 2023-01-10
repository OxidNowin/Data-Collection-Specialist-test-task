# - *- coding: utf- 8 - *-
from aiogram import types


start_reply_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
start_reply_kb.row('🎤 Конвертировать аудиосообщение')
start_reply_kb.row('🖼️ Определить лицо на фото')

cancel_reply_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
cancel_reply_kb.row('⛔ Отмена')
