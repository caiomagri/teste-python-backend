import urllib
import logging
import requests

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def get_result_from_google_search():
    url = 'https://www.google.com/search?q=caixa+mega+sena'

    request = urllib.request.Request(url)

    request.add_header('User-Agent',
                       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 '
                       '(KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')

    raw_response = urllib.request.urlopen(request).read()

    html = raw_response.decode("utf-8")
    soup = BeautifulSoup(html, 'html.parser')

    data = soup.findAll("span", attrs={"class": "zSMazd"})

    result_list = []

    if data:
        result_list = [int(span.text) for span in data]

    logger.warning(f"Resultado do webscrapping Google - {result_list}")

    return result_list


def get_result_from_cef():
    html = requests.get("http://www.loterias.caixa.gov.br/wps/portal/loterias").content
    soup = BeautifulSoup(html, 'html.parser')

    data = soup.find("ul", attrs={"class": "resultado-loteria mega-sena"})

    result_list = []

    if data:
        result_list = [int(li.text) for li in data.findAll("li")]

    logger.warning(f"Resultado do webscrapping Caixa Economica Federal - {result_list}")

    return result_list


def get_lottery_result():
    response = get_result_from_google_search() or get_result_from_cef()
    if not response:
        raise Exception("Não foi possível realizar o webscraping do resultado da mega sena")
    return response
