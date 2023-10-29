from queue import Empty
import sqlite3
import threading


def truncate_target_table(func):
    def wrapper(*args):
        db_path = args[0].db_path
        table_name = args[0].table_name
        try:
            conn = sqlite3.connect(db_path)
            conn.execute(f"DELETE FROM {table_name}")
            conn.commit()
            conn.close()
            print(f"Successfully cleaned up {table_name}")
        except:
            print(f"Error truncating {table_name}")
            raise
        func(*args)

    return wrapper


class SQLiteScheduler(threading.Thread):
    db_path = "stocks.db"
    table_name = "prices"

    def __init__(self, id, input_queue, **kwargs):
        super().__init__(**kwargs)
        self.id = id
        self.input_queue = input_queue
        self.start()

    @truncate_target_table
    def run(self):
        while True:
            try:
                val = self.input_queue.get(timeout=10)
            except Empty:
                break
            if val == "DONE":
                break
            symbol, price, extraction_time = val

            if symbol and price:
                conn = sqlite3.connect("stocks.db")
                worker = SQLiteWorker(symbol, price, extraction_time, conn)
                worker.insert_data()


class SQLiteWorker:
    target_table = "prices"

    def __init__(self, symbol, price, extraction_time, conn):
        self.symbol = symbol
        self.price = price
        self.extraction_time = extraction_time
        self.conn = conn

    def insert_data(self):
        print(f"Processing {self.symbol}, {self.price}")
        query = f"INSERT INTO {SQLiteWorker.target_table} (symbol, price, extraction_time) VALUES ('{self.symbol}', {self.price}, '{self.extraction_time}')"
        print(query)
        try:
            self.conn.execute(query)
            self.conn.commit()
            self.conn.close()
            print("Values inserted successfully")
        except:
            print("Error inserting values")
            raise
