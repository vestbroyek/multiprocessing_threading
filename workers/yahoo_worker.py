import random
import threading
import requests
from lxml import html
import time
from queue import Empty
import datetime

import threading
import datetime
import random
from queue import Empty

class YahooScheduler(threading.Thread):
    """
    A class for scheduling YahooFinanceWorker tasks on a separate thread.

    Args:
        input_queue (queue.Queue): A queue of tasks to be processed.
        output_queue (list or queue.Queue): A list of output queues to put the results in.

    Attributes:
        input_queue (queue.Queue): A queue of tasks to be processed.
        output_queues (list): A list of output queues to put the results in.

    Methods:
        run(): The main method of the thread. Retrieves tasks from the input queue, processes them using
              YahooFinanceWorker, and puts the results in the output queues.
    """
    def __init__(self, input_queue, output_queue, **kwargs):
        super().__init__(**kwargs)
        self.input_queue = input_queue
        temp_queue = output_queue
        if not isinstance(output_queue, list):
            temp_queue = [output_queue]
        self.output_queues = temp_queue
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

            yahoo_worker= YahooFinanceWorker(task) # Create a YahooFinanceWorker object for the task
            price = yahoo_worker.run() # Retrieve the stock price using the YahooFinanceWorker object
            for output_queue in self.output_queues: # Put the output values into each output queue
                output_values = (task, price, datetime.datetime.utcnow())
                output_queue.put(output_values)
            time.sleep(random.random()) # Sleep for a random amount of time to simulate processing time


class YahooFinanceWorker(threading.Thread):
    """
    A class representing a worker that extracts company information from Yahoo Finance.

    Attributes:
    -----------
    symbol : str
        The stock symbol of the company to extract information for.
    url : str
        The URL of the Yahoo Finance page for the given stock symbol.
    """

    def __init__(self, symbol: str, **kwargs):
        """
        Initializes a new instance of the YahooFinanceWorker class.

        Parameters:
        -----------
        symbol : str
            The stock symbol of the company to extract information for.
        **kwargs : dict
            Additional keyword arguments to pass to the threading.Thread constructor.
        """
        super().__init__(**kwargs)
        self.symbol = symbol
        base_url = "https://finance.yahoo.com/quote/"
        self.url = base_url + symbol
        self.start()

    def _extract_company_info(self, page_html: str) -> float:
        """
        Extracts the current price of the company from the given HTML page.

        Parameters:
        -----------
        page_html : str
            The HTML content of the Yahoo Finance page for the given stock symbol.

        Returns:
        --------
        float
            The current price of the company.
        """
        tree = html.fromstring(page_html)
        company_price = float(tree.xpath("//*[@id=\"quote-header-info\"]/div[3]/div[1]/div[1]/fin-streamer[1]")[0].text)
        return company_price

    def run(self):
        """
        Runs the worker thread, extracting the current price of the company from the Yahoo Finance page.
        """
        time.sleep(0.5)
        response = requests.get(self.url, headers={"User-Agent":"Mozilla/5.0"})
        if response.status_code == 200:
            price = self._extract_company_info(response.text)
            return price
        else:
            print(f"Failed to get SP500 from {self.url}")
            print(response.status_code)