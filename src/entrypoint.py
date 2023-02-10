"""
THIS IS ENTRY POINT FOR WEB-HOOK REQUESTS
DO NOT MOVE FROM ROOT LOCATION
"""
import telebot
from src.context import global_context


def run_bot(message):
    from src.main import bot
    bot.process_new_updates([message])


def handler(event, context):
    message = telebot.types.Update.de_json(event['body'])
    global_context.set_context(context.context.token)
    run_bot(message)
    return {
        'statusCode': 200,
        'body': '!',
    }


if __name__ == "__main__":
    """
    Точка входа для продакшен окружения, не использовать для локального развертывания
    """
    global_context.set_context_from_env()
    from src.main import bot
    bot.infinity_polling()

