import requests
from bs4 import BeautifulSoup
import re

url = "https://www2.correios.com.br/sistemas/rastreamento/ctrl/ctrlRastreamento.cfm?"
data = {
    "acao": "track",
    # Código de rastreio aqui no formato AA000000000AA
    "objetos": "AA000000000AA"
}

page = requests.post(url=url, data=data)
soup = BeautifulSoup(markup=page.content, features='html.parser')

events = soup.find_all(name='table', attrs={'class': 'listEvent sro'})

print('Rastreio do código ' + data['objetos'] + ':')

if len(events) == 0:
    print('Código não encontrado na base dos Correios BR.')

for event in events:
    date_raw = event.find_all(name="td", attrs={'class': 'sroDtEvent'})[0].text
    date = re.search(r"[0-9]{2}/[0-9]{2}/[0-9]{4}", date_raw)[0]

    time = re.search(r"[0-9]{2}:[0-9]{2}", date_raw)[0]

    location_raw = date_raw.replace('\n', '').replace('\r', '').replace('\t', '')
    location = re.search(r"(?<=:[0-9]{2}).*", location_raw)[0].strip()

    event_raw = event.find_all(name="td", attrs={'class': 'sroLbEvent'})[0].text
    event_raw = re.sub('\t+', ' ', event_raw)
    event_raw = re.sub('\n+', ' ', event_raw)
    event_raw = re.sub('\r+', ' ', event_raw)
    event_raw = re.sub('\s+', ' ', event_raw)
    event_str = event_raw.strip()

    info_index = event_str.find('Informar')
    if info_index != -1:
        point_index = info_index - 1
        event_str = event_str[:point_index] + '.' + event_str[point_index:]

    print(f'{date} {time} - {location}:')
    print(event_str)
    print('')
