# - *- coding: utf- 8 - *-
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

import config
from dispatcher import dp, bot
from filters import IsAdmin
from keyboards import *
from utils import is_user, add_user, add_file_path
from states import *

import datetime
import logging
import dlib
import ffmpeg
import os


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if not is_user(message.from_user.id):
        add_user(message.from_user.id)
    await message.bot.send_message(message.chat.id,
                                   f"Привет, {message.from_user.first_name.title()}\n",
                                   reply_markup=start_reply_kb)


@dp.message_handler(commands=['menu'])
async def menu(message: types.Message):
    await message.bot.send_message(message.chat.id, "Главное меню:", reply_markup=start_reply_kb)


@dp.message_handler(Text(equals='🖼️ Определить лицо на фото'))
async def get_photo(message: types.Message):
    await GetImage.image.set()
    await message.bot.send_message(message.chat.id, "Отправьте фото:", reply_markup=cancel_reply_kb)


@dp.message_handler(Text(equals='🎤 Конвертировать аудиосообщение'))
async def get_audio(message: types.Message):
    await GetAudio.audio.set()
    await message.bot.send_message(message.chat.id, "Отправьте аудиосообщение:", reply_markup=cancel_reply_kb)


@dp.message_handler(state='*', commands='⛔ Отмена')
@dp.message_handler(Text(equals='⛔ Отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info(f'From {message.from_user.id}\nCancelling state {current_state}\nAt {datetime.datetime.now()}\n\n')
    await state.finish()
    await message.reply('Отмена...', reply_markup=start_reply_kb)


@dp.message_handler(content_types='photo', state=GetImage.image)
async def check_photo(message: types.Message, state: FSMContext):
    num_files = len([f for f in os.listdir('./saved_images/')
                     if os.path.isfile(os.path.join('./saved_images/', f))])
    file_path = f"./saved_images/image_{message.from_user.id}_{num_files}.jpg"
    await message.photo[-1].download(destination_file=file_path)
    detector = dlib.get_frontal_face_detector()
    img = dlib.load_rgb_image(file_path)
    dets = detector(img, 1)
    if len(dets) > 0:
        ans = "На фото кто-то есть"
        add_file_path(message.from_user.id, 'photo', file_path)
    else:
        ans = "На фото не удалось распознать лицо"
        os.remove(file_path)
    await state.finish()
    await message.bot.send_message(message.chat.id,
                                   ans,
                                   reply_markup=start_reply_kb)


@dp.message_handler(state=GetImage.image)
async def get_photo_invalid(message: types.Message):
    await message.bot.send_message(message.chat.id,
                                   "Отправьте изображение!",
                                   reply_markup=cancel_reply_kb)


@dp.message_handler(content_types='voice', state=GetAudio.audio)
async def check_audio(message: types.Message, state: FSMContext):
    voice = await message.voice.get_file()
    path = "./saved_audios"
    converted_path = "./converted_audios"

    num_raw_files = len([f for f in os.listdir(path)
                         if os.path.isfile(os.path.join(path, f))])

    num_converted_files = len([f for f in os.listdir(converted_path)
                               if os.path.isfile(os.path.join(converted_path, f))])

    destination = f"{path}/{message.from_user.id}_{num_raw_files}.ogg"
    converted_destination = f'./converted_audios/audio_message_{num_converted_files}.wav'

    await bot.download_file(file_path=voice.file_path, destination=destination)
    out_put = (
        ffmpeg
        .input(destination)
        .output(converted_destination, format='wav', ac=1, ar='16k')
        .overwrite_output()
        .run()
    )

    add_file_path(message.from_user.id, 'raw_voice', destination)
    add_file_path(message.from_user.id, 'converted_voice', converted_destination)
    await state.finish()
    await message.bot.send_message(message.chat.id,
                                   "ans",
                                   reply_markup=start_reply_kb)


@dp.message_handler(state=GetAudio.audio)
async def get_audio_invalid(message: types.Message):
    await message.bot.send_message(message.chat.id,
                                   "Отправьте аудиосообщение!",
                                   reply_markup=cancel_reply_kb)
