from aiogram import types, Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F

from rich import print

from aiogram_dialog import DialogManager

import asyncio

from loads.loadbeatinl import Beat, background


from ext import dtb
from config import shop_channel_id, project_channel_id





comrout = Router()


@comrout.callback_query(F.data=="cancel_load", StateFilter(Beat.file))
async def cancelload(call: types.CallbackQuery, dialog_manager: DialogManager):

    await call.answer("Загрузка бита отменена")
    await dialog_manager.dialog_data.clear()


@comrout.callback_query(F.data=="cancel_load", StateFilter(None))
async def cancelload(call: types.CallbackQuery, dialog_manager: DialogManager):

    await call.answer("Ты ничего не загружаешь")



@comrout.callback_query(F.data=="loadbeat")
async def waitmp3inl(call: types.CallbackQuery, dialog_manager: DialogManager):

    await dialog_manager.start(Beat.bar)
    


@comrout.message(Command("loadbeat"))
async def waitmp3(message: Message, dialog_manager: DialogManager):

    await dialog_manager.start(Beat.bar)




@comrout.message(Command("test"))
async def prtest(message: Message, dialog_manager: DialogManager):

    await dialog_manager.start(Beat.bar)
    asyncio.create_task(background(dialog_manager.bg()))
    await dialog_manager.next()
