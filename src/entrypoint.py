import telebot
from src.constants import global_context


def run_bot(message):
    from src.main import bot
    bot.process_new_updates([message])


def handler(event, context):
    message = telebot.types.Update.de_json(event['body'])
    global_context.set_context(context)
    run_bot(message)
    return {
        'statusCode': 200,
        'body': '!',
    }
