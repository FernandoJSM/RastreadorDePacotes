import requests
from bs4 import BeautifulSoup
import re

url = "https://www2.correios.com.br/sistemas/rastreamento/ctrl/ctrlRastreamento.cfm?"
data = {
    "acao": "tracks",
    # Código de rastreio aqui no formato AA000000000AA separado por ";"
    # Rastreio de até 50 códigos!
    "objetos": "AA000000000AA; AA000000000AA; AA000000000AA"
}

print('Rastreio dos códigos ' + data['objetos'] + ':\n')

# Remove os espaços e ; para entrar no sistema dos correios
aux_codes = re.sub('\s+', '', data['objetos'])
data['objetos'] = re.sub(';+', '', aux_codes)

page = requests.post(url=url, data=data)
soup = BeautifulSoup(markup=page.content, features='html.parser')

tables = soup.find_all(name="td")

if len(tables) == 0:
    print('Resultado não encontrado na base dos Correios BR.')

for i_e in range(len(tables) // 3):
    code_raw = tables[i_e * 3].text
    code = re.sub('\n+', '', code_raw)

    event = tables[i_e * 3 + 1].text
    date_loc = tables[i_e * 3 + 2].text

    print(f'{code} - {date_loc}: {event}')
