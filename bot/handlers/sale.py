from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from bot.keyboards.sale_keyboards import base_sale_keyboards

router = Router(name="Распродажи")


@router.callback_query(F.data == "sale_panel")
async def back_sale(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.message.edit_text(text=f"⌛️ Ручной парсинг был: 03.01.2025 в 15:30",
                                              reply_markup=base_sale_keyboards())







