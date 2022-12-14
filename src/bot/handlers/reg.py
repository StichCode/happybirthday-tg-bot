import re
from datetime import datetime

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from dependency_injector.wiring import inject, Provide

from src.bot.time import _to_datetime
from src.container import Container
from src.dto.user import User
from src.storage.cache import Cache


@inject
async def _reg(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    cache: Cache = Provide[Container.cache]
) -> None:
    """
    Registration user with Optional argument for birthday

    using:
        /reg            - save without birthday

        /reg {date_arg: str | optional}

        ### format mm{./-}dd{./-}YYYY
        /reg 01.01.2001 - save with birthday
        /reg 01/01/2001 - save with birthday
        /reg 01-01-2001 - save with birthday

    :param update:
    :param context:
    :return:
    """
    key = (update.effective_user.id, update.effective_chat.id)
    user = await cache.get(key)
    dt = re.findall(r'\d{2}[./-]\d{2}[./-]\d{4}', context.args[0]) if context.args else None

    ny = datetime.now().year
    # ToDo: refactoring
    if (context.args and len(context.args) > 1) or \
        (context.args and not dt) or \
        (dt and ny - _to_datetime(dt[0]).year < 18):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Уважаемый <i>{}</i> вводите валидный формат данных'.format(
                update.effective_user.name),
            parse_mode='HTML'
        )
        return
    if user and update.effective_user.name:
        user.name = update.effective_user.name
        await cache.set(user)

    if user and dt and dt != user.birthday:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Вы {0} уверены, что хотите заменить {1} на {2} дату?'.format(
                user.name,
                user.birthday.strftime('%d.%m.%Y') if user.birthday else 'None',
                dt[0]
            ),
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton("Да", callback_data='1'),
                        InlineKeyboardButton("Нет", callback_data='0')
                    ]
                ],
                one_time_keyboard=True
            )
        )
        context.user_data[key] = _to_datetime(dt[0])
        return
    elif user and not dt and user.birthday:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Вы уже зарегистрировались',
            parse_mode='HTML'
        )
        return
    else:
        user = User(
            tg_id=update.effective_user.id,
            group_id=update.effective_chat.id,
            name=update.effective_user.name,
            birthday=_to_datetime(dt)
        )
        await cache.set(user)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=user.__str__(), parse_mode='HTML')
