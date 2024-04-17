from aiogram.types import Message
from aiogram.filters import CommandObject
from core.db.db_utils import unban_user, ban_user, delete_user

async def ban(message: Message, command: CommandObject):
    if not command.args.isdigit():
        await message.answer("Введите id пользователя")
        return
    if command.args: #Если аргументов нет -> None
        result = ban_user(int(command.args)) # Если пользователя с таким id нет или он забанен -> False, иначе -> True
        if result:
            await message.answer("Пользователь забанен")
        else:
            await message.answer("Пользователь не забанен")

async def unban(message: Message, command: CommandObject):
    if not command.args.isdigit():
        await message.answer("Введите id пользователя")
        return
    if command.args: #Если аргументов нет -> None
        result = unban_user(int(command.args)) # Если пользователя с таким id нет или он не забанен -> False, иначе -> True
        if result:
            await message.answer("Пользователь разбанен")
        else:
            await message.answer("Пользователь не разбанен")

async def delete(message: Message, command: CommandObject):
    if not command.args.isdigit():
        await message.answer("Введите id пользователя")
        return
    if command.args: #Если аргументов нет -> None
        result = delete_user(int(command.args)) # Если пользователя с таким id нет -> False, иначе -> True
        if result:
            await message.answer("Пользователь удален")
        else:
            await message.answer("Пользователь не удален")