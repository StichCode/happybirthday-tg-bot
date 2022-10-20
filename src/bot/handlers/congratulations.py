import logging
import re
import sys
import traceback

from loguru import logger
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from dependency_injector.wiring import inject, Provide

from src.bot.time import _to_datetime
from src.container import Container
from src.dto.user import User
from src.storage.cache import Cache


@inject
async def _callbacks_congratulations(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    cache: Cache = Provide[Container.cache]
) -> None:
    q = update.callback_query
    await q.answer()
    try:
        some_id = int(q.data)
    except ValueError as ex:
        # send message about server error
        logger.error(ex)
        return

    chat = context.bot.get_chat(some_id)

    pattern = '{}_*' if some_type != 'group' else '*_{}'
    try:
        keys = await cache.keys(pattern=pattern)
        keys = [k.split('_') for k in keys]
        if not keys:
            return
    except Exception as ex:
        logger.error(ex)
        return

    members = [
        await context.bot.get_chat_member(
            some_id, k[1]
        ) for k in keys
    ]

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Итак вы захотели кого то поздравить, давайте сначала выберем чат:',
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(chat.title, callback_data=chat.id)
                    for chat in members
                    if chat.type == chat.GROUP
                ]
            ],
            one_time_keyboard=True
        )
    )


@inject
async def _congrat(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    cache: Cache = Provide[Container.cache]
) -> None:
    """
    Registration user with Optional argument for birthday
    """
    keys = await cache.keys('{}_*'.format(update.effective_user.id))
    keys = [k.split('_') for k in keys]

    if not keys:
        # no keys return that need registr
        return
    chats = [c for c in [await context.bot.get_chat(k[1]) for k in keys] if c.type == c.GROUP]

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Итак вы захотели кого то поздравить, давайте сначала выберем чат:',
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(chat.title, callback_data=chat.id)
                    for chat in chats
                ]
            ],
            one_time_keyboard=True
        )
    )
