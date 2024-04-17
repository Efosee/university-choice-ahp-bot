from core.db.db_utils import write_user, UserDB, check_user
from dictionary import dictionary
from aiogram.types import Message


async def start(message: Message):
    if check_user(message.from_user.id) == None:
        user = UserDB(user_id=message.from_user.id,
                      chat_id=message.chat.id,
                      username=message.from_user.username,
                      first_name=message.from_user.first_name,
                      last_name=message.from_user.last_name
                      )
        write_user(user)
        first_name = message.from_user.first_name
        await message.answer(f'Привет, {first_name}! {dictionary["first_start"]}')
    else:
        await message.answer(dictionary["repeat_start"])

async def help(message: Message):
    pass

async def info(message: Message):
    pass
