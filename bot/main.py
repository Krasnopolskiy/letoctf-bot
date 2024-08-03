import structlog
from config.bot import bot
from dialogs.register import register_dialogs
from dispatcher import dp
from routers.register import register_routers

structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S", utc=False),
        structlog.dev.ConsoleRenderer(),
    ],
    logger_factory=structlog.PrintLoggerFactory(),
)

logger = structlog.get_logger()


def main():
    logger.info("Start telegram bot")
    try:
        register_dialogs()
        register_routers()
        dp.run_polling(bot.bot)
    finally:
        logger.info("Stop telegram bot")


if __name__ == "__main__":
    main()
