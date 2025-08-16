from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from apps.bot.keyboards.parsing_sale_keyboards import parsing_sale_keyboards
from apps.parser.service.last_pars import get_last_pars
from config import regions, regions_name
from config_bot import repo_manager

router = Router(name="Распродажи")


@router.callback_query(F.data == "sale_panel")
async def back_sale(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    _,_, last_pars_date = await get_last_pars(repo_manager=repo_manager)
    country = await repo_manager.country_repo.get_all_county_pars_sale()
    region_text = "Регионы для копирования цен:\n"
    for region in regions:
        if country.get(region):
            region_text += regions_name.get(region) + "\n"
    await callback_query.message.edit_text(text=f"⌛️ Парсинг был: {last_pars_date}\n\n" + region_text,
                                              reply_markup=parsing_sale_keyboards())







