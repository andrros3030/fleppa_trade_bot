import telebot
from src.main import bot
from src.constants import update_db_user_password


def handler(event, context):
    message = telebot.types.Update.de_json(event['body'])
    update_db_user_password(context.token["access_token"])
    bot.process_new_updates([message])
    return {
        'statusCode': 200,
        'body': '!',
    }
