from bs4 import BeautifulSoup
from decimal import Decimal
import requests


def convert(amount, cur_from, cur_to, date, requests):
    url = "http://www.cbr.ru/scripts/XML_daily.asp"
    params = {"date_req": date}
    response = requests.get(url, params)
    soup = BeautifulSoup(response.text, "lxml")
    currencies = soup.find_all("valute")

    _from = get_exchange_info(cur_from, currencies)
    _to = get_exchange_info(cur_to, currencies)
    result = amount * _from / _to
    return result.quantize(Decimal('.0001'))


def get_exchange_info(name_currency, currencies):
    if name_currency == "RUR":
        return 1
    for currency in currencies:
        if currency.charcode.text == name_currency:
            nominal = int(currency.nominal.text)
            value = Decimal(currency.value.text.replace(",", "."))
            return value / nominal

# correct = Decimal('3754.8057')
# result = convert(Decimal("1000.1000"), 'RUR', 'JPY', "17/02/2005", requests)
# if result == correct:
#     print("Correct")
#     print(result)
# else:
#     print("Incorrect: %s != %s" % (result, correct))