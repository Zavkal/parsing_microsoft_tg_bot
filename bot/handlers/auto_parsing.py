from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from bot.keyboards.auto_parsing_keyboards import auto_parsing_keyboards, settings_auto_parsing_keyboards

router = Router(name="Автопарсинг")


@router.callback_query(F.data == "base_auto_parsing")
async def parsing_sale_(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.message.edit_text(text=f"Тут типо показывает что у нас в автопарсинге",
                                              reply_markup=auto_parsing_keyboards())


@router.callback_query(F.data == "settings_auto_parsing")
async def parsing_sale_(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.message.edit_text(text=f"Тут типо настройки автопарса",
                                              reply_markup=settings_auto_parsing_keyboards())