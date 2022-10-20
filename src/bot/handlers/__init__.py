from typing import Any

from telegram.ext import ContextTypes, CommandHandler, CallbackContext, CallbackQueryHandler

from src.bot.handlers.callbacks import _callback_reg_query
from src.bot.handlers.commands import _reg, _users_info, _fullness_check, _test_try, _choose_sex, _help
from src.bot.handlers.congratulations import _congrat, _callbacks_congratulations


def get_handlers() -> list[CommandHandler[CallbackContext | Any]]:
    # ToDo: add handler to set timezone
    return [
        CommandHandler('reg', _reg),
        CommandHandler('info', _users_info),
        CommandHandler('fullness', _fullness_check),
        CommandHandler('test', _test_try),
        CommandHandler('sex', _choose_sex),
        CommandHandler('help', _help),
        CommandHandler('cong', _congrat),
        CallbackQueryHandler(_callbacks_congratulations),
        CallbackQueryHandler(_callback_reg_query)
    ]
