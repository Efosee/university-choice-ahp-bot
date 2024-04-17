from aiogram.types import Message, CallbackQuery
from aiogram import Bot
from aiogram.fsm.context import FSMContext
from core.redis.storage import storage
from aiogram.fsm.storage.redis import StorageKey
from core.keyboards.inline import inline_vuz, fc_inline_vuz, AddingList
from dictionary import dictionary
async def message_builder(caption: str, words_list):
    mes = caption
    for word in words_list:
        mes += "\n" + word
    return mes

async def start_calculation(message: Message, bot: Bot, state: FSMContext):
    await message.answer(dictionary["enter_vuz"])
    # Рудимент
    # await bot.send_message(message.from_user.id, "Сейчас введи название первого ВУЗа")
    await state.set_state("entering_fc_vuz")

async def restart_calculation(chat_id, bot: Bot, state: FSMContext):
    text = dictionary["enter_vuz_cancel"]
    await bot.send_message(chat_id, text)
    await state.set_state("entering_fc_vuz")

async def entering_fc_vuz(message: Message, state: FSMContext, bot: Bot):
    data = {"VUZ": [message.text]}
    key = StorageKey(bot.id, message.chat.id, message.from_user.id)
    await storage.set_data(key=key, data=data)
    data = await storage.get_data(key=key)
    text = await message_builder("<b>Выбранные ВУЗы:</b>", data["VUZ"])
    await message.answer(text=text, reply_markup=fc_inline_vuz)
    await state.set_state("entering_next_vuz")

async def callback_processing(call: CallbackQuery, callback_data: AddingList, bot:Bot, state: FSMContext):
    key = StorageKey(bot.id, call.message.chat.id, call.from_user.id)
    if callback_data.action == "add":
        data = await storage.get_data(key=key)
        text = await message_builder("<b>Выбранные ВУЗы:</b>", data["VUZ"])
        text += "\n\n<b><i>Введите следующий вуз</i></b>"
        await bot.edit_message_text(text=text, chat_id=call.message.chat.id, message_id=call.message.message_id)
        data["edit_mes"] = {"chat_id":call.message.chat.id, "message_id":call.message.message_id}
        await storage.set_data(key=key, data=data)
        return
    #if callback_data.action == "next":
    #Убираем InlineKeyboard, чтобы пользователь не мог отправить запрос дважды
    await call.message.edit_text(text=call.message.text, reply_markup=None)
    text = dictionary["second_wave"]
    await bot.send_message(chat_id=call.message.chat.id, text=text)
    await state.set_state("entering_fc_criteria")

async def callback_cancel(call: CallbackQuery, callback_data: AddingList, bot:Bot, state: FSMContext):
    key = StorageKey(bot.id, call.message.chat.id, call.from_user.id)
    if await state.get_state() == "entering_next_vuz":
        await storage.set_data(key=key, data={})
        await call.message.delete()
        await restart_calculation(chat_id=call.from_user.id, state=state, bot=bot)
async def entering_next_vuz(message: Message, bot: Bot, state: FSMContext):
    key = StorageKey(bot.id, message.chat.id, message.from_user.id)
    data = await storage.get_data(key=key)
    data["VUZ"].append(message.text)
    text = await message_builder("<b>Выбранные ВУЗы:</b>", data["VUZ"])
    #TODO возможно доделать, чтобы не приходилось каждый раз нажимать на кнопку "добавить"
    #text += "\n\n<b><i>Введите следующий вуз</i></b>"
    await bot.edit_message_text(text=text, chat_id=data["edit_mes"]["chat_id"], message_id=data["edit_mes"]["message_id"],
                                reply_markup=inline_vuz())
    await message.delete()
    await storage.set_data(key=key, data=data)


