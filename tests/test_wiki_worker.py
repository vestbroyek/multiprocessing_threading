import unittest
from workers.wiki_worker import WikiWorker


class TestWikiWorker(unittest.TestCase):
    def test_get_sp_500(self):
        worker = WikiWorker()
        symbols = list(worker.get_sp_500())
        self.assertGreater(len(symbols), 0)
        self.assertTrue(
            all(isinstance(symbol, str) and len(symbol) > 0 for symbol in symbols)
        )
