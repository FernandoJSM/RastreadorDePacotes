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
aux_codes = re.sub(r'\s+', '', data['objetos'])
data['objetos'] = re.sub(';+', '', aux_codes)

page = requests.post(url=url, data=data)
soup = BeautifulSoup(markup=page.content, features='html.parser')

tables = soup.find_all(name="td")

if len(tables) == 0:
    print('Resultado não encontrado na base dos Correios BR.')

not_found_str = 'O nosso sistema não possui dados sobre o objeto informado.'

for td in tables:
    find_code = re.match(pattern=r'[A-Za-z]{2}[0-9]{9}[A-Za-z]{2}',
                         string=re.sub(pattern=r'\n+', repl='', string=td.text))
    find_date = re.match(pattern=r'[0-9]{2}/[0-9]{2}/[0-9]{4}',
                         string=td.text)
    not_found = td.text.find(not_found_str)

    if find_code:
        tracking_code = find_code.string
    else:
        if not_found != -1:
            print(f'{tracking_code}: \t{not_found_str}')
        else:
            if find_date:
                print(f'{tracking_code} - \t{find_date.string}: \t{event_str}')
            else:
                event_str = td.text
