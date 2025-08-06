import asyncio

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from service.save_data import save_data_in_list

router = Router(name="Кнопки получения файлов")


@router.callback_query(F.data == "output_data_sale")
async def output_data_sale(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.answer()
    await save_data_in_list()
    await asyncio.sleep(1)
    # Отправляем документ
    await callback_query.bot.send_document(
        chat_id=callback_query.from_user.id,
        caption='Файл',
        document=FSInputFile('games_prices.txt')
    )