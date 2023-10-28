import time
import queue
from workers.sqlite_worker import SQLiteScheduler
from workers.wiki_worker import WikiWorker
from workers.yahoo_worker import YahooScheduler

if __name__ == "__main__":
    # setup
    symbol_queue = queue.Queue()
    sql_queue = queue.Queue()

    # Get start time
    scraper_start = time.time()
    
    # Create the wiki worker
    wiki_worker = WikiWorker()

    # Yahoo set up
    yahoo_price_scheduler_threads = []
    num_yahoo_workers = 12
    for i in range(num_yahoo_workers):
        yahoo_scheduler = YahooScheduler(id=i, input_queue=symbol_queue, output_queue=sql_queue)
        yahoo_price_scheduler_threads.append(yahoo_scheduler)

    # SQL set up
    sql_scheduler_threads = []
    num_sql_workers = 2
    for i in range(num_sql_workers):
        sql_scheduler = SQLiteScheduler(id=i, input_queue=sql_queue)
        sql_scheduler_threads.append(sql_scheduler)

    symbol_counter = 0
    for symbol in wiki_worker.get_sp_500():
        symbol_queue.put(symbol)

    # Yahoo threads
    for i in range(len(yahoo_price_scheduler_threads)):
        symbol_queue.put("DONE")

    for i in range(len(yahoo_price_scheduler_threads)):
        yahoo_price_scheduler_threads[i].join()

    for i in range(len(sql_scheduler_threads)):
        sql_scheduler_threads[i].join()

    print(f"Scraper finished in {time.time() - scraper_start} seconds.")
