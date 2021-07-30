from urllib.request import Request, urlopen
import logging
import requests

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

TIMEOUT = 20


def get_result_from_google_search() -> list:
    """
    Função para realizar o Webscrapping no Google, formatar os dados em uma lista de inteiros e
    retornar.

    :return: [ int ]
    """
    result_list = []

    try:
        url = 'https://www.google.com/search?q=caixa+mega+sena'

        request = Request(url)

        request.add_header('User-Agent',
                           'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 '
                           '(KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')

        raw_response = urlopen(request, timeout=TIMEOUT).read()

        html = raw_response.decode("utf-8")
        soup = BeautifulSoup(html, 'html.parser')

        data = soup.findAll("span", attrs={"class": "zSMazd"})

        if data:
            result_list = [int(span.text) for span in data]
        logger.warning(f"Webscrapping Google Result - {result_list}")

    except Exception as ex:
        logger.error(f"ERROR Webscraping Google - {str(ex)}")

    return result_list


def get_result_from_cef() -> list:
    """
    Função para realizar o Webscrapping na Caixa Econômica Federal, formatar os dados em uma lista de inteiros e
    retornar.

    :return: [ int ]
    """

    result_list = []

    try:
        url = "http://www.loterias.caixa.gov.br/wps/portal/loterias"

        html = requests.get(url, timeout=TIMEOUT).content
        soup = BeautifulSoup(html, 'html.parser')

        data = soup.find("ul", attrs={"class": "resultado-loteria mega-sena"})

        if data:
            result_list = [int(li.text) for li in data.findAll("li")]

        logger.warning(f"Webscrapping CEF Result - {result_list}")
    except Exception as ex:
        logger.error(f"ERROR Webscraping CEF - {str(ex)}")

    return result_list


def get_lottery_result() -> list:
    """
    Função core para realizar a consulta dos resultado da mega sena, tentando fazer o webscrapping no Google ou na
    Caixa Econômica Federal.

    :return: [ int ]
    """

    response = get_result_from_google_search() or get_result_from_cef()
    if not response:
        raise Exception("It was not possible to get the result of the mega sena")
    return response
