from aiogram.types import Message, CallbackQuery
from aiogram import Bot
import json
from aiogram.fsm.context import FSMContext
from core.redis.storage import storage
from core.keyboards.inline import Compare, inline_compare
from core.utils.ahpy_calculate import calculate_target_weights, result_calculator
from aiogram.fsm.storage.redis import StorageKey


async def compare_criteria(bot: Bot, chat_id, user_id):
    key = StorageKey(bot.id, chat_id, user_id)
    data = await storage.get_data(key=key)
    fc = data["criteria"][data["vector_i"]]  # first criteria
    nc = data["criteria"][data["vector_j"]]  # next criteria
    text = f"Сравниваем <b>{fc}</b> с {nc}"
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=inline_compare(int(data["vector_i"])))

async def record_compare(call: CallbackQuery, callback_data: Compare, bot: Bot, state: FSMContext):
    key = StorageKey(bot.id, call.message.chat.id, call.from_user.id)
    data = await storage.get_data(key=key)
    data["criteria_comparisons"][json.dumps((data["criteria"][data["vector_i"]], data["criteria"][data["vector_j"]]))] = callback_data.value
    data["vector_j"] = data["vector_j"] + 1
    #Удаление первого критерия в списке и обнуление вектора
    if data["vector_j"] == (len(data["criteria"])):
        if data["vector_i"] != (len(data["criteria"]) - 2):
            data["vector_i"] += 1
            data["vector_j"] = data["vector_i"] + 1
        else:
            #обнуление векторов (возврат в начальное положение)
            data["vector_i"] = 0
            data["vector_j"] = 1
            data["vector_g"] = 0
            data["vuz_comparisons"] = {}
            data["vuz_comparisons"][data["criteria"][data["vector_g"]]] = {}
            await storage.set_data(key=key, data=data)
            await state.set_state("compare_vuz")
            await bot.edit_message_text(text=f"{call.message.text}\n", chat_id=call.message.chat.id,
                                        message_id=call.message.message_id, reply_markup=None)
            return await compare_vuz(bot, call.message.chat.id, call.from_user.id)
    #TODO Ошибка в том, что ключом redis может быть только TypeError: keys must be str, int, float, bool or None, not tuple
    #TODO Выбранное решение - json.dumps() -> переделывает в str. Далее loads() -> возвращает списки, т.к в json нет кортежей
    #TODO Т.к. ключи в словаре должны быть не изменяемые, переделываем их в tuple (кортеж)
    #TODO На будущее можем создать высокоспециализированный кодировщик и перехват декодера https://stackoverflow.com/questions/15721363/preserve-python-tuples-with-json

    await storage.set_data(key=key, data=data)
    await bot.edit_message_text(text=f"{call.message.text}\n",chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
    await compare_criteria(bot, call.message.chat.id, call.from_user.id)


async def compare_vuz(bot: Bot, chat_id, user_id):
    key = StorageKey(bot.id, chat_id, user_id)
    data = await storage.get_data(key=key)
    fv = data["VUZ"][data["vector_i"]]  # first VUZ
    nv = data["VUZ"][data["vector_j"]]  # next VUZ
    cr = data["criteria"][data["vector_g"]]  # criteria
    text = f"Сравниваем по критерию <b>{cr}</b> \n<b>{fv}</b> с {nv}"
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=inline_compare(int(data["vector_i"])))

async def record_compare_vuz(call: CallbackQuery, callback_data: Compare, bot: Bot, state: FSMContext):
    key = StorageKey(bot.id, call.message.chat.id, call.from_user.id)
    data = await storage.get_data(key=key)
    data["vuz_comparisons"][data["criteria"][data["vector_g"]]][json.dumps((data["VUZ"][data["vector_i"]], data["VUZ"][data["vector_j"]]))] = callback_data.value
    data["vector_j"] += 1
    #Удаление первого критерия в списке и обнуление вектора
    if data["vector_j"] == (len(data["VUZ"])):
        if data["vector_i"] != (len(data["VUZ"]) - 2):
            data["vector_i"] += 1
            data["vector_j"] = data["vector_i"] + 1
        elif data["vector_g"] != (len(data["criteria"]) - 1):
            data["vector_i"] = 0
            data["vector_j"] = 1
            data["vector_g"] += 1
            data["vuz_comparisons"][data["criteria"][data["vector_g"]]] = {}
        else:
            data["criteria_comparisons"] = {tuple(json.loads(key)): value for key, value in data["criteria_comparisons"].items()}
            data["vuz_comparisons"] = {key: {tuple(json.loads(k)): v for k, v in value.items()} for key, value in data["vuz_comparisons"].items()}
            target_weights = await calculate_target_weights(data)
            text = await result_calculator(target_weights)
            await bot.edit_message_text(text=f"{call.message.text}\n", chat_id=call.message.chat.id,
                                        message_id=call.message.message_id, reply_markup=None)
            return await bot.send_message(chat_id=call.message.chat.id, text=text)
    await storage.set_data(key=key, data=data)
    await bot.edit_message_text(text=f"{call.message.text}\n", chat_id=call.message.chat.id,
                                message_id=call.message.message_id, reply_markup=None)
    await compare_vuz(bot, call.message.chat.id, call.from_user.id)