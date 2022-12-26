from src.constants import set_testing_mode


def run():
    from src.main import bot, logger
    bot.remove_webhook()
    logger.v('pre-start loading is complete')
    logger.v('local infinity_polling is started')
    bot.infinity_polling()


set_testing_mode()
run()
