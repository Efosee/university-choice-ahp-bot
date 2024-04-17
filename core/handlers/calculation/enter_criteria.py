from aiogram.types import Message, CallbackQuery
from aiogram import Bot
from aiogram.fsm.context import FSMContext
from core.redis.storage import storage
from aiogram.fsm.storage.redis import StorageKey
from core.keyboards.inline import inline_vuz, fc_inline_criteria, AddingList
from core.handlers.calculation.enter_vuz import message_builder
from core.handlers.calculation.calculation import compare_criteria
from dictionary import dictionary

async def restart_criteria(chat_id, bot: Bot, state: FSMContext):
    text = dictionary["enter_criteria_cancel"]
    await bot.send_message(chat_id, text)
    await state.set_state("entering_fc_criteria")

async def entering_fc_criteria(message: Message, state: FSMContext, bot: Bot):
    key = StorageKey(bot.id, message.chat.id, message.from_user.id)
    data = await storage.get_data(key=key)
    data["criteria"] = [message.text]
    await storage.set_data(key=key, data=data)
    text = await message_builder("<b>Выбранные критерии:</b>", data["criteria"])
    await message.answer(text=text, reply_markup=fc_inline_criteria)
    await state.set_state("entering_next_criteria")
async def callback_processing_criteria(call: CallbackQuery, callback_data: AddingList, bot:Bot, state: FSMContext):
    key = StorageKey(bot.id, call.message.chat.id, call.from_user.id)
    if callback_data.action == "add":
        data = await storage.get_data(key=key)
        text = await message_builder("<b>Выбранные критерии:</b>", data["criteria"])
        text += "\n\n<b><i>Введите следующий критерий</i></b>"
        await bot.edit_message_text(text=text, chat_id=call.message.chat.id, message_id=call.message.message_id)
        data["edit_mes"] = {"chat_id":call.message.chat.id, "message_id":call.message.message_id}
        await storage.set_data(key=key, data=data)
        return
    #if callback_data.action == "next":
    await call.message.edit_reply_markup(reply_markup=None)
    text = dictionary["third_wave"]
    await bot.send_message(chat_id=call.message.chat.id, text=text)
    await state.set_state("compare_criteria")
    data = await storage.get_data(key=key)
    data["vector_i"] = 0
    data["vector_j"] = 1
    data["criteria_comparisons"] = {}
    await storage.set_data(key=key, data=data)
    await compare_criteria(bot, call.message.chat.id, call.from_user.id)


async def callback_cancel_criteria(call: CallbackQuery, callback_data: AddingList, bot:Bot, state: FSMContext):
    key = StorageKey(bot.id, call.message.chat.id, call.from_user.id)
    if await state.get_state() == "entering_next_criteria":
        print(1)
        data = await storage.get_data(key=key)
        del data["criteria"]
        await storage.set_data(key=key, data=data)
        await call.message.delete()
        await restart_criteria(chat_id=call.from_user.id, state=state, bot=bot)

async def entering_next_criteria(message: Message, bot: Bot, state: FSMContext):
    key = StorageKey(bot.id, message.chat.id, message.from_user.id)
    data = await storage.get_data(key=key)
    data["criteria"].append(message.text)
    text = await message_builder("<b>Выбранные критерии:</b>", data["criteria"])
    await bot.edit_message_text(text=text, chat_id=data["edit_mes"]["chat_id"], message_id=data["edit_mes"]["message_id"],
                                reply_markup=inline_vuz("критерий"))
    await message.delete()
    await storage.set_data(key=key, data=data)

