from datetime import datetime

from loguru import logger

from telegram.ext import ContextTypes
from dependency_injector.wiring import Provide

from src.container import Container
from src.bot.birthday_utils import check_birthday, create_birthday_message
from src.storage.cache import Cache


async def birthday_notify(
    context: ContextTypes.DEFAULT_TYPE,
    cache: Cache = Provide[Container.cache]
) -> None:
    """
    Notify about birthday of users

    :return:
    """
    timezone = context.bot.defaults.tzinfo
    now = datetime.now(tz=timezone).date()
    try:
        data = await cache.dall_users()
    except Exception as ex:
        logger.exception(ex)
        return

    if not data:
        logger.info('No data from cache')
        return
    pretty_data = check_birthday(data, current_date=now)
    if not pretty_data:
        logger.info('No birthdays today')
        return

    for chat_id, birthdays in pretty_data.items():
        text = create_birthday_message(birthdays)
        try:
            await context.bot.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode='HTML'
            )
        except Exception as ex:
            logger.error(ex)
            # ToDo(stichcode): send msg admin if error or sentry?
