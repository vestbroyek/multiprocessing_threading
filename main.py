import time
import queue
from workers.wiki_worker import WikiWorker
from workers.yahoo_worker import YahooScheduler

if __name__ == "__main__":

    # setup 
    symbol_queue = queue.Queue()
    scraper_start = time.time()
    wiki_worker = WikiWorker()

    yahoo_price_scheduler_threads = []
    num_yahoo_workers = 8

    for i in range(num_yahoo_workers):
        yahoo_scheduler = YahooScheduler(id = i, input_queue=symbol_queue)
        yahoo_price_scheduler_threads.append(yahoo_scheduler)

    for symbol in wiki_worker.get_sp_500():
        symbol_queue.put(symbol)

    for i in range(len(yahoo_price_scheduler_threads)):
        symbol_queue.put('DONE')

    for i in range(len(yahoo_price_scheduler_threads)):
        yahoo_price_scheduler_threads[i].join()

    print(f"Scraper finished in {time.time() - scraper_start} seconds.")