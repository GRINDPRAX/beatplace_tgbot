from aiogram import types, Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from rich import print


from aiogram_dialog.widgets.text import Const, Jinja, Format, Multi, Progress
from aiogram_dialog import (
    Dialog, DialogManager, setup_dialogs, Window, BaseDialogManager
)
from aiogram_dialog.widgets.kbd import Checkbox, Next, SwitchTo, Radio, ScrollingGroup, Button, Back, Row
from aiogram_dialog.widgets.input import MessageInput, TextInput

import random, asyncio

from ext import dtb
from config import shop_channel_id, project_channel_id


states = {}


async def setton(call, wid, mng, _):
    mng.dialog_data['ton'] = _

    return True

async def setgenre(call, wid, mng, _):
    mng.dialog_data['genre'] = _

    return True

async def setlead(call, wid, mng, _):
    mng.dialog_data['lead'] = _

    return True

async def setmood(call, wid, mng, _):
    mng.dialog_data['mood'] = _

    return True


toncs = [Radio(
    Format("💥 {item}"),
    Format("{item}"),
    items=["F", "Dm", "C", "Am", "G", "Em", "D", "Bm", "A", "F#m", "E", "C#m", "Bc♭", "G#m",
           "G#m", "G♭#F", "E♭m", "D♭c#", "A♭", "Fm", "E♭", "Cm", "B♭", "Gm"],
    item_id_getter=lambda x: x,
    id="r_ton",
    on_click=setton
)]

genres = [
    Radio(
        Format("⚡️ {item}"),
        Format("{item}"),
        items=['Rap', 'Drill', "Hyperpop", 'UK Drill', 'New Jersey', 'Jersey club', 'Phonk', 'Rock',
               'Memphis', 'EDM', 'SynthWave'],
        item_id_getter=lambda x: x,
        id="r_genre",
        on_click=setgenre
    )
]

leads = [Radio(
        Format("💫 {item}"),
        Format("{item}"),
        items=['Piano`s', 'Guitar`s', "Fluite`s", '808`s', 'Chord`s', 'Bell`s', 'Other`s'],
        item_id_getter=lambda x: x,
        id="r_lead",
        on_click=setlead
    )]


moods = [Radio(
        Format("🎧 {item}"),
        Format("{item}"),
        items=['Happy', 'Sad', "Agressive", 'Vibe'],
        item_id_getter=lambda x: x,
        id="r_mood",
        on_click=setmood
    )]





















inlload = Router()


class Beat(StatesGroup):
    bar = State()

    file = State()
    bpm = State()
    ton = State()
    genre = State()
    lead = State()
    mood = State()
    options = State()
    price = State()
    proj = State()
    
    prew = State()

    



async def next_or_end(event: types.Message, widget, dialog_manager: DialogManager, *_):

    if widget.widget.widget_id == 'bpm':
        try:

            bpm = int(event.text)
            await dialog_manager.next()

        except Exception as e:
            await event.answer(f"Ошибка {e}\n\nУкажи целое число")


    elif widget.widget.widget_id == 'price':
        options = []
        full ,cmr, read = 0, 0, 0
        prcs = 0
        if dialog_manager.find("fullap").is_checked():
            full = 1
            prcs+=1
        if dialog_manager.find("readonl").is_checked():
            read = 1
            prcs+=1
        if dialog_manager.find("leaz").is_checked():
            cmr = 1
            prcs+=1
        


        try:
            prices = event.text.split(' ', prcs)
            if len(prices) == prcs:
                for price in prices:
                    if " " in price:
                        await event.answer(f"Введи цены через пробел, только для указанных вариантов")
                        return
                    else:
                        price = int(price)
                        if full and full<200: full = price
                        elif cmr and cmr<100: cmr = price
                        elif read and read<50: read = price
                        else:
                            await event.answer("Введи цены в порядке: за полные права, за аренду, за изучение (Если какого-то пункта нет - проупскай)\n\nМинимальная цена для\n\t•Только для изучения: 50р\n\t•Аренда: 100Р\n\t•Полные права: 200Р")
                            return            
                dialog_manager.dialog_data['full'] = full
                dialog_manager.dialog_data['cmr'] = cmr
                dialog_manager.dialog_data['read'] = read
                await dialog_manager.next()
            else:
                await event.answer(f"Введи цены через пробел, только для указанных вариантов")
                return
        
        except ValueError:
            print(f"[purple]{e}")
            await event.answer(f"Ошибка {e}\n\nУкажи целое число")
        except Exception as e:
            await event.answer(f"Ошибка {e}")


    
async def get_bg_data(dialog_manager: DialogManager, **kwargs):
    return {
        "progress": dialog_manager.dialog_data.get("progress", 0)
    }


async def background(manager: BaseDialogManager):
    count = 20
    for i in range(1, count + 1):
        await asyncio.sleep(1)
        await manager.update({
            "progress": i * 100 / count,
        })
    await asyncio.sleep(0.3)
    await manager.done()



@inlload.message(Beat.file)
async def getbeat(message: types.Message, wid: MessageInput, aiogram_dialog: DialogManager):
    if hasattr(message, "audio") or (hasattr(message, 'document') and message.document.mime_type == 'audio/vnd.wave'):
       
        if message.audio:       
            await message.bot.download(
                message.audio,
                destination=f"./beats/{message.from_user.id}.mp3"
            )
            aiogram_dialog.dialog_data['beat'] = message.audio.file_id
        else:
            await message.bot.download(
                message.document,
                destination=f"./beats/{message.from_user.id}.wav"
            )
            aiogram_dialog.dialog_data['beat'] = message.document.file_id

        await message.answer("Бит скачан")
        await aiogram_dialog.next()
        return
    bldr = InlineKeyboardBuilder()
    bldr.add(
        types.InlineKeyboardButton(text="Отменить", callback_data="cancel_load")
        )
    await message.answer("Ошибка! Отправь файл mp3/wav или нажми отменить", reply_markup=bldr.as_markup())





















@inlload.message(Beat.proj)
async def getproj(message: types.Message, wid: MessageInput, aiogram_dialog: DialogManager):
    if (hasattr(message, 'document') and message.document.mime_type == 'application/zip'):
        if message.document:

            path_proj = message.document.file_id
            pthfolder = f"./projes/{message.from_user.id}_{random.randint(1, 100000)}.zip"
            await message.bot.download(
                message.document,
                destination=pthfolder
            )
            

            await message.answer("Проект скачан")
            aiogram_dialog.dialog_data['project'] = path_proj
            await aiogram_dialog.next()
            return
    
    bldr = InlineKeyboardBuilder()
    bldr.add(
        types.InlineKeyboardButton(text="Отменить", callback_data="cancel_load")
        )
    await message.answer("Ошибка! Отправь проект в формате ZIP или нажми отменить", reply_markup=bldr.as_markup())










FINISHED_KEY = 'finished'


CANCEL_EDIT = SwitchTo(
    Const("Подтвердить"),
    when=F["dialog_data"][FINISHED_KEY],
    id="cnl_edt",
    state=Beat.prew,
)


async def result_getter(dialog_manager: DialogManager, **kwargs):
    dialog_manager.dialog_data[FINISHED_KEY] = True
    options = []
    if dialog_manager.find("fullap").is_checked():
        options.append("Полные права")
    if dialog_manager.find("readonl").is_checked():
        options.append("Только для изучения")
    if dialog_manager.find("leaz").is_checked():
        options.append("Аренда")

    prcs = dialog_manager.find("price").get_value()
    full, commerc, read = 0, 0, 0
    text = "\n"
    if dialog_manager.find("fullap").is_checked():
        full = 1
        fullp = dialog_manager.dialog_data['full']
        text += f"\t\t• Полные права: {dialog_manager.dialog_data['full']}Р\n"
    if dialog_manager.find("readonl").is_checked():
        read = 1
        readp = dialog_manager.dialog_data['read']
        text += f"\t\t• Только для изучения: {dialog_manager.dialog_data['read']}Р\n"
    if dialog_manager.find("leaz").is_checked():
        commerc = 1
        cmrp = dialog_manager.dialog_data['cmr']
        text += f"\t\t• Аренда: {dialog_manager.dialog_data['cmr']}Р"
    
    return {
        "options": options,
        "bpm": dialog_manager.find("bpm").get_value(),
        "ton": dialog_manager.dialog_data['ton'],
        "genre": dialog_manager.dialog_data['genre'],
        "lead": dialog_manager.dialog_data['lead'],
        "mood": dialog_manager.dialog_data['mood'],
        "price": text
    }



async def sendbeat(message: types.CallbackQuery, wid: MessageInput, aiogram_dialog: DialogManager):
    text = f"#{aiogram_dialog.dialog_data['genre']} / #{aiogram_dialog.dialog_data['ton']} - #{aiogram_dialog.find('bpm').get_value()} BPM\n\nЦена:"
    full, commerc, read = 0, 0, 0
    fullp, readp, cmrp = 0, 0, 0
    if aiogram_dialog.find("fullap").is_checked():
        full = 1
        fullp = aiogram_dialog.dialog_data['full']
        text += f"\t\t• Полные права: {aiogram_dialog.dialog_data['full']}"
    if aiogram_dialog.find("readonl").is_checked():
        read = 1
        readp = aiogram_dialog.dialog_data['read']
        text += f"\t\t• Только для изучения: {aiogram_dialog.dialog_data['read']}"
    if aiogram_dialog.find("leaz").is_checked():
        commerc = 1
        cmrp = aiogram_dialog.dialog_data['cmr']
        text += f"\t\t• Аренда: {aiogram_dialog.dialog_data['cmr']}"

    aud = aiogram_dialog.dialog_data['beat']
    proj = aiogram_dialog.dialog_data['project']
    

    msg1 = await message.bot.send_audio(chat_id=shop_channel_id, audio=aud, caption=text)

    msg_id = msg1.message_id

    msg2 = await message.bot.send_document(chat_id=project_channel_id, document= proj,
    caption=f"{message.from_user.id}")

    proj_id = msg2.message_id
    
        

    await dtb.regbeat(msg_id, proj_id, message.from_user.id, fullp, cmrp, readp,)


    pass

dlg = Dialog(
    Window(
            Multi(Const("Загружаю файл"), Progress("progress", 20, filled="█", empty="▒")),
            state=Beat.bar,
            getter=get_bg_data
        ),
    Window(
        Const("Отправь файл с битом WAV/MP3"),
        MessageInput(func=getbeat),
        CANCEL_EDIT,
        state=Beat.file,
        ),
    Window(
        Const("Напиши BPM бита"),
        TextInput(id='bpm', on_success=next_or_end),
        CANCEL_EDIT,
        state=Beat.bpm
    ),
    Window(
        Const("Выбери тональность бита"),
        ScrollingGroup(*toncs, id="rton", width=4, height=3, hide_on_single_page=True),
        Row(Back(Const("Назад")), Next(Const("Далее"))),
        CANCEL_EDIT,
        state=Beat.ton,
    ),
    Window(
        Const("Выбери жанр"),
        ScrollingGroup(*genres, id="rgenre", width=4, height=3, hide_on_single_page=True),
        Row(Back(Const("Назад")), Next(Const("Далее"))),
        CANCEL_EDIT,
        state=Beat.genre
    ),
    Window(
        Const("Выбери Инструмент"),
        ScrollingGroup(*leads, id="rlead", width=4, height=3, hide_on_single_page=True),
        Row(Back(Const("Назад")), Next(Const("Далее"))),
        CANCEL_EDIT,
        state=Beat.lead
    ),
    Window(
        Const("Выбери Настроение"),
        ScrollingGroup(*moods, id="rmood", width=4, height=3, hide_on_single_page=True),
        Row(Back(Const("Назад")), Next(Const("Далее"))),
        CANCEL_EDIT,
        state=Beat.mood
    ),
    Window(
        Const("Выбери возможные варианты продажи бита"),
        Checkbox(Const("💎Полные права"), Const("Полные права"), id='fullap'),
        Checkbox(Const("💎Только для изучения"), Const("Только для изучения"), id='readonl'),
        Checkbox(Const("💎Аренда"), Const("Аренда"), id='leaz'),
        Row(Back(Const("Назад")), Next(Const("Далее"))),
        CANCEL_EDIT,
        state=Beat.options
    ),
    Window(
        Const("Введи цену бита в рублях"),
        TextInput(id='price', on_success=next_or_end),
        CANCEL_EDIT,
        state=Beat.price
    ),
    Window(
        Const("Отправь проект бита"),
        MessageInput(func=getproj),
        CANCEL_EDIT,
        state=Beat.proj
    ),
    Window(
        Jinja(
            "<u>Вы ввели</u>:\n\n"
            "<b>BPM</b>: {{bpm}}\n"
            "<b>Тональность</b>: {{ton}}\n"
            "<b>Жанр</b>: {{genre}}\n"
            "<b>Инструмент</b>: {{lead}}\n"
            "<b>Настроение</b>: {{mood}}\n"
            "<b>Цена</b>: {{price}}\n"
            "<b>Варианты продажи</b>: \n"
            "{% for item in options %}"
            "• {{item}}\n"
            "{% endfor %}",
        ),
        Row(
            SwitchTo(
                Const("Изменить BPM"),
                state=Beat.bpm, id='to_bpm'
            ),
            SwitchTo(
                Const("Изменить тональность"),
                state=Beat.ton, id='to_ton'
            )
        ),
        Row(
            SwitchTo(
                Const("Изменить жанр"),
                state=Beat.genre, id='to_genre'
            ),
            SwitchTo(
                Const("Изменить цену"),
                state=Beat.price, id='to_price'
        )
        ),
        SwitchTo(
            Const("Изменить настроение"),
            state=Beat.mood, id='to_mood'
        ),
        SwitchTo(
            Const("Изменить инструмент"),
            state=Beat.lead, id='to_lead'
        ),
        
        SwitchTo(
            Const("Изменить варианты продажи"),
            state=Beat.options, id='to_options'
        ),
        Button(
            Const("💸Отправить бит"),
            id='acceptsend',
            on_click=sendbeat
        ),

        getter=result_getter,
        state=Beat.prew
    )
)











