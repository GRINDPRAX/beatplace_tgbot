import logging, asyncio

from loads import loadbeat, loadbeatinl

from aiogram import F
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from aiogram_dialog import (
    Dialog, DialogManager, setup_dialogs, StartMode, Window,
)

from config import *
from ext.dtb import *

from aiogram.fsm.storage.memory import MemoryStorage

storage = MemoryStorage()

dp = Dispatcher(storage=storage)




@dp.message(Command('start'))
async def start(message: types.Message):

    bldr = InlineKeyboardBuilder()
    
    print(message.text)

    bldr.row(types.InlineKeyboardButton(text="Личный кабинет", callback_data="userinf"))

    bldr.row(types.InlineKeyboardButton(text="Продать", callback_data="loadbeat"), types.InlineKeyboardButton(text="Купить", url=buychannel))
    bldr.row(types.InlineKeyboardButton(text="Тех. поддрежка", url=support))


    if await check(message.from_user.id):
        await reg(message.from_user.id, message.from_user.first_name)

    await message.reply(f"Салам { message.from_user.first_name}", reply_markup=bldr.as_markup())

    













async def main() -> None:
    bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp.include_router(loadbeatinl.inlload)
    dp.include_router(loadbeatinl.dlg)
    setup_dialogs(dp)
    #dp.include_router(loadbeat.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await createDB()
    await dp.start_polling(bot)
    


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())