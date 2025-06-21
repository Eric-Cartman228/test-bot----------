import os
import io
import logging
import asyncio
from datetime import datetime
import pandas as pd
import aiohttp

from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
from sqlalchemy.ext.asyncio import AsyncSession
from services import get_all_data

router = Router()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


async def send_file_with_retries(
    callback: CallbackQuery, file: FSInputFile, attempts=5
):
    for i in range(attempts):
        try:
            await callback.message.answer_document(file)
            logger.info(f"Файл успешно отправлен с попытки {i + 1}")
            return True
        except aiohttp.ClientConnectionError:
            delay = 2**i
            logger.warning(f"Ошибка соединения. Попытка {i + 1}. Ждём {delay} сек...")
            await asyncio.sleep(delay)
        except Exception as e:
            logger.error(f"Неожиданная ошибка при отправке: {e}")
            return False
    return False


@router.callback_query(F.data == "watch_list_of_users")
async def watch_list_of_users(callback: CallbackQuery, session: AsyncSession):
    data = await get_all_data(session)
    logger.info(f"Получено {len(data)} записей")

    user_dict = {}
    for row in data:
        key = (row[0], row[1], row[2], row[3])
        if key not in user_dict:
            user_dict[key] = []
        if row[4] is not None:
            date_activate = row[5] if row[5] is not None else "-"
            date_expired = row[6] if row[6] is not None else "-"
            user_dict[key].append((row[4], date_activate, date_expired))

    for i, (user_info, subs) in enumerate(user_dict.items(), start=1):
        username, user_id, phone, email = user_info

        if subs:
            subs_text = "\n".join(
                [
                    f'- Подписка: "{s[0]}", Дата выдачи: {s[1]}, Дата отключения: {s[2]}'
                    for s in subs
                ]
            )
        else:
            subs_text = "- Подписки нет"

        # await callback.message.answer(
        # f"""{i}. Пользователь: {username}
    # - ID пользователя: {user_id}
    # - Телефон: {phone}
    # - Gmail: {email}
    # {subs_text}"""
    # )
    await send_users_file(callback, data)


async def send_users_file(callback: CallbackQuery, data):
    df = pd.DataFrame(
        [
            {
                "№": i + 1,
                "Пользователь": row[0] or "",
                "ID": row[1] or "",
                "Телефон": row[2] or "",
                "Gmail": row[3] or "",
                "Подписка": row[4] or "",
                "Дата выдачи": row[5] if row[5] is not None else "-",
                "Дата отключения": row[6] if row[6] is not None else "-",
            }
            for i, row in enumerate(data)
        ]
    )

    output = io.BytesIO()
    df.to_excel(
        output, index=False, engine="openpyxl", sheet_name="Users & Subscriptions"
    )
    output.seek(0)

    # Сохраняем локальную копию
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    local_filename = f"users_and_subscriptions_{timestamp}.xlsx"
    df.to_excel(local_filename, index=False, engine="openpyxl")
    logger.info(f"Локальная копия сохранена: {local_filename}")

    # Пробуем отправить из памяти
    file = FSInputFile(output, filename="users_and_subscriptions.xlsx")
    success = await send_file_with_retries(callback, file)

    if not success:
        logger.info("Пробуем отправить локальный файл...")
        file = FSInputFile(local_filename)
        success = await send_file_with_retries(callback, file, attempts=3)

    #     if success:
    #         await callback.message.answer(
    #             f"Файл успешно отправлен. Локальная копия сохранена: {local_filename}"
    #         )
    #     else:
    #         await callback.message.answer(
    #             f"⚠️ Не удалось отправить файл. Локальная копия сохранена: {local_filename}"
    #         )
    # else:
    #     await callback.message.answer(
    #         f"Файл успешно отправлен. Локальная копия сохранена: {local_filename}"
    #     )

    output.close()
    os.remove(file.filename)
