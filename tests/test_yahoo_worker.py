import unittest
from workers.wiki_worker import WikiWorker
from workers.yahoo_worker import YahooFinanceWorker

class TestYahooFinanceWorker(unittest.TestCase):
    def setUp(self):
        # Fetch a list of symbols from the WikiWorker
        wiki_worker = WikiWorker()
        self.symbols = wiki_worker.get_sp_500()

    def test_symbols(self):
        # Test all valid symbols
        current_workers = []
        for i, symbol in enumerate(self.symbols):
            yahoo_worker = YahooFinanceWorker(thread_id=i, symbol=symbol)
            current_workers.append(yahoo_worker)

        for i in range(len(current_workers)):
            current_workers[i].join()


if __name__ == '__main__':
    unittest.main()