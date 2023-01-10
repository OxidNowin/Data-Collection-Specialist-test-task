# - *- coding: utf- 8 - *-
from aiogram.dispatcher.filters.state import State, StatesGroup


class GetAudio(StatesGroup):
    audio = State()


class GetImage(StatesGroup):
    image = State()
