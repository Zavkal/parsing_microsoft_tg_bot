from aiogram import F, Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from bot.keyboards.base_menu_keyboards import base_menu_keyboards

router = Router(name="Начальная работа с постом")


@router.message(CommandStart())
async def command_start_handler(message: types.Message):
    await message.delete()

    await message.bot.send_message(chat_id=message.chat.id,
                                   text=f"Настройки автопарсинга:\n"
                                        f"✅ Новинки: Каждый день в 12:00.\n"
                                        f"✅ Распродажи: Каждый вторник в 14:10.\n"
                                        f"❌ Общая база: Выключено",
                                   reply_markup=base_menu_keyboards())


@router.callback_query(F.data == "back_base_menu_keyboards")
async def command_start_handler(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(text=f"Настройки автопарсинга:\n"
                                        f"✅ Новинки: Каждый день в 12:00.\n"
                                        f"✅ Распродажи: Каждый вторник в 14:10.\n"
                                        f"❌ Общая база: Выключено",
                                   reply_markup=base_menu_keyboards())

