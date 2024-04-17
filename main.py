import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import Command, StateFilter
from aiogram.client.default import DefaultBotProperties

from core.redis.storage import storage
from core.utils.config import config
from core.handlers.users import start
from core.handlers.admins import ban, unban, delete
from core.handlers.calculation.enter_vuz import start_calculation, entering_fc_vuz, entering_next_vuz, callback_processing, callback_cancel
from core.handlers.calculation.enter_criteria import callback_processing_criteria, entering_fc_criteria, entering_next_criteria, callback_cancel_criteria
from core.handlers.calculation.calculation import record_compare, record_compare_vuz
from core.middlewaries.isbanned import IsBanned
from core.filters.isadmin import IsAdminFilter
from core.keyboards.inline import AddingList, Compare
bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher(storage=storage)

async def main():
    dp.update.middleware.register(IsBanned())
    dp.message.register(start, Command("start"))
    dp.message.register(ban, Command("ban"), IsAdminFilter())
    dp.message.register(unban, Command("unban"), IsAdminFilter())
    dp.message.register(delete, Command("del"), IsAdminFilter())

    dp.message.register(start_calculation, Command("calc"))
    dp.message.register(entering_fc_vuz, StateFilter("entering_fc_vuz"))
    dp.callback_query.register(callback_processing, StateFilter("entering_next_vuz"), AddingList.filter(F.action.in_(["add", "next"])))
    dp.callback_query.register(callback_cancel, StateFilter("entering_next_vuz"), AddingList.filter(F.action == "cancel"))
    dp.message.register(entering_next_vuz, StateFilter("entering_next_vuz"))

    dp.message.register(entering_fc_criteria, StateFilter("entering_fc_criteria"))
    dp.callback_query.register(callback_processing_criteria, StateFilter("entering_next_criteria"), AddingList.filter(F.action.in_(["add", "next"])))
    dp.callback_query.register(callback_cancel_criteria, StateFilter("entering_next_criteria"), AddingList.filter(F.action == "cancel"))
    dp.message.register(entering_next_criteria, StateFilter("entering_next_criteria"))

    dp.callback_query.register(record_compare, StateFilter("compare_criteria"), Compare.filter())
    dp.callback_query.register(record_compare_vuz, StateFilter("compare_vuz"), Compare.filter())
    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        await dp.stop_polling()
    finally:
        await dp.stop_polling()

if __name__ == '__main__':
    asyncio.run(main())