import random
import threading
import requests
from lxml import html
import time
from queue import Empty
from requests.exceptions import ConnectionError

class YahooScheduler(threading.Thread):

    def __init__(self, id, input_queue, **kwargs):
        super().__init__(**kwargs)
        self.id = id
        self.input_queue = input_queue
        self.start()

    def run(self):
        """
        The main method of the thread. Retrieves tasks from the input queue, processes them using
        YahooFinanceWorker, and puts the results in the output queues.
        """
        while True:
            try:
                task = self.input_queue.get(timeout=10) # Get a task from the input queue
            except Empty:
                print('Yahoo queue is empty')
                break
            if task == 'DONE': # If the task is 'DONE', stop the thread
                break

            yahoo_worker = YahooFinanceWorker(thread_id = self.id, symbol=task) 
            price = yahoo_worker.get_price()
            print(self.id, " ", task, " ", price)
            time.sleep(random.random())


class YahooFinanceWorker():

    def __init__(self, thread_id, symbol: str, **kwargs):
        super().__init__(**kwargs)
        self.thread_id = thread_id
        self.symbol = symbol
        base_url = "https://finance.yahoo.com/quote/"
        self.url = base_url + symbol

    def _extract_company_info(self, page_html: str) -> float:
        tree = html.fromstring(page_html)
        try:
            company_price = tree.xpath("//*[@id=\"quote-header-info\"]/div[3]/div[1]/div[1]/fin-streamer[1]")[0].text
            if company_price:
                company_price = company_price.replace(',', '')
                return company_price
        except ConnectionError:
            print(f"Thread ID {self.thread_id} raised a connection error")

    def get_price(self):
        time.sleep(0.2)
        response = requests.get(self.url, headers={"User-Agent":"Mozilla/5.0"})
        if response.status_code == 200:
            price = self._extract_company_info(response.text)
            return price
        else:
            print(f"Failed to get SP500 from {self.url}")
            print(response.status_code)