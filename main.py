import asyncio
import logging

from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncEngine
from database import db_helper

from middleware import DBSessionMiddleware

from database.models import Base

from aiogram import Bot,Dispatcher
from core import BOT_TOKEN

@asynccontextmanager
async def lifespan():
    async with db_helper.engine.begin() as conn:
        # Optional: drop all tables
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield
    finally:
        await db_helper.engine.dispose()



bot=Bot(token=BOT_TOKEN)
dp=Dispatcher()

@dp.startup()
async def on_startup(dispatcher:Dispatcher):
    dispatcher['lifespan_cm']=lifespan()
    await dispatcher['lifespan_cm'].__aenter__()
    print('Db initialized')
    

@dp.shutdown()
async def on_shutdown(dispatcher: Dispatcher):
    await dispatcher['lifespan_cm'].__aexit__(None,None,None)
    print('Bd connected closed')

db_session_middleware = DBSessionMiddleware(db_helper)
dp.message.middleware(db_session_middleware)
dp.callback_query.middleware(db_session_middleware)


logger=logging.getLogger(__name__)

async def main():
    await dp.start_polling(bot)

if __name__=='__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except (KeyboardInterrupt,SystemExit):
        print('Бот выключен')
    except Exception as err:
        logger.exception(f"Возникла ошибка: {err}")
