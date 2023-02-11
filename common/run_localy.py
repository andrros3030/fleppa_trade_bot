from src.common_modules.run_context import global_context


def run():
    from src.main import bot, logger
    bot.remove_webhook()
    logger.v('pre-start loading is complete')
    logger.v('local infinity_polling is started')
    bot.infinity_polling()


global_context.set_testing_mode()
run()
