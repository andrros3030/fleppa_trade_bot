from src.main import bot, logger
from src.constants import WEBHOOK

res = bot.set_webhook(WEBHOOK)
logger.v("Webhook set-up complete: " + str(res))
