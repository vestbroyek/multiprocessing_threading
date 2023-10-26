import sqlite3
import threading


class SQLiteScheduler(threading.Thread):
    def __init__(self, id, input_queue, **kwargs):
        super().__init__(**kwargs)
        self.id = id
        self.input_queue = input_queue
        self.start()

    def run(self):
        while True:
            val = self.input_queue.get()
            if val == "DONE":
                break
            symbol, price, extraction_time = val
            worker = SQLiteWorker(symbol, price, extraction_time)
            worker.insert_data()


class SQLiteWorker:
    def __init__(self, symbol, price, extraction_time):
        self.symbol = symbol
        self.price = price
        self.extraction_time = extraction_time

    def insert_data(self):
        query = f"INSERT INTO stock_data (symbol, price, extraction_time) VALUES ({self.symbol}, {self.price}, {self.extraction_time})"
        conn = sqlite3.connect("../database/stocks.db")
        conn.execute(query)
