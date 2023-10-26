import requests
from bs4 import BeautifulSoup


class WikiWorker:
    def __init__(self) -> None:
        self._url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

    @staticmethod
    def _extract_company_symbols(page_html):
        soup = BeautifulSoup(page_html, "lxml")
        table = soup.find(id="constituents")
        rows = table.find_all("tr")
        for row in rows[1:]:
            symbol = row.find("td").text.strip("\n")
            yield symbol

    def get_sp_500(self):
        response = requests.get(self._url)
        if response.status_code == 200:
            yield from self._extract_company_symbols(response.text)
        else:
            raise Exception(f"Failed to get SP500 from {self._url}")
