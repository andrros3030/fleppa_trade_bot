from src.common.context import global_context


def run():
    from src.main import bot, logger
    res = bot.set_webhook(global_context.WEBHOOK)
    logger.v("Webhook set-up complete: " + str(res))


global_context.set_testing_mode()
run()
