import sys

from loguru import logger

from app.core.sqlite_log_sink import SQLiteLogSink


def setup_logging():
    logger.remove()

    logger.add(sys.stdout, format="{time:HH:mm:ss} | {level} | {message}", level="INFO")

    # SQLite log sink
    sqlite_sink = SQLiteLogSink()
    logger.add(sqlite_sink, serialize=False, level="INFO")

    return logger
