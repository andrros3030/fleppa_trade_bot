import telebot
from src.main import bot
from src.constants import global_context


def handler(event, context):
    message = telebot.types.Update.de_json(event['body'])
    global_context.set_context(context)
    bot.process_new_updates([message])
    return {
        'statusCode': 200,
        'body': '!',
    }
