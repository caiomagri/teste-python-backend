import requests

from bs4 import BeautifulSoup


def get_lottery_result():
    html = requests.get("http://www.loterias.caixa.gov.br/wps/portal/loterias").content
    soup = BeautifulSoup(html, 'html.parser')

    ul_result = soup.find("ul", attrs={"class": "resultado-loteria mega-sena"})

    if not ul_result:
        pass

    result_list = [int(li.text) for li in ul_result.findAll("li")]

    return result_list
