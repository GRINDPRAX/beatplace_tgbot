from aiogram import types, Router
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message



router = Router()




@router.message(Command("loadbeat"))
async def loadbeathan(message: types.Message, bot: Bot):

    await message.reply("loadni beat svoi")


    