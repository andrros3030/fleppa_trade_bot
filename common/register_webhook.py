from src.main import bot, logger
from src.constants import global_context

res = bot.set_webhook(global_context.WEBHOOK)
logger.v("Webhook set-up complete: " + str(res))
