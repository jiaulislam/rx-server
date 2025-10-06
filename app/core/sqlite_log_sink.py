import json
import sqlite3
import threading
from queue import Empty, Queue
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from loguru import Message


class SQLiteLogSink:
    def __init__(self, db_path: str = "log.db"):
        self.db_path = db_path
        self.queue = Queue()
        self._setup_database()
        self.worker_thread = threading.Thread(target=self._process_queue, daemon=True)
        self.worker_thread.start()

    def _setup_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS rx_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                level TEXT,
                message TEXT,
                extra JSON
            )
            """
        )
        conn.commit()
        conn.close()

    def _process_queue(self):
        while True:
            try:
                log_entry = self.queue.get(timeout=1)
                self._insert_log(**log_entry)
            except Empty:
                continue

    def _insert_log(self, time: str, level: str, message: str, extra: dict):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Serialize extra dict to JSON string
        extra_json = json.dumps(extra) if extra else "{}"

        cursor.execute(
            "INSERT INTO rx_logs (timestamp, level, message, extra) VALUES (?, ?, ?, ?)",
            (time, level, message, extra_json),
        )
        conn.commit()
        conn.close()

    def __call__(self, log_record: "Message"):
        record = log_record.record
        self.queue.put(
            {
                "time": record["time"].strftime("%Y-%m-%d %H:%M:%S.%f"),
                "level": record["level"].name,
                "message": record["message"],
                "extra": record["extra"],
            }
        )
