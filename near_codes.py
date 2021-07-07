import requests
from bs4 import BeautifulSoup
import re
from datetime import date
from typing import List


def web_scrape_tracking_data(tracking_code_list: List[str], skip_not_found: bool, first_index:int):
    """
        Get a code list and print the results obtained from the Correios BR website
    Args:
        tracking_code_list (List[str]): String with a list of tracking codes separated with a semicolon
        skip_not_found (bool): Skip the print of tracking results that are not found
        first_index (int): Index of the row to be printed
    """

    url = 'https://www2.correios.com.br/sistemas/rastreamento/ctrl/ctrlRastreamento.cfm?'
    data = {
        'acao': 'tracks',
        'objetos': ''.join(tracking_code_list)
    }

    page = requests.post(url=url, data=data)
    soup = BeautifulSoup(markup=page.content, features='html.parser')

    tables = soup.find_all(name='td')

    if len(tables) == 0:
        print('Resultado não encontrado na base dos Correios BR.')

    not_found_str = 'O nosso sistema não possui dados sobre o objeto informado.'
    today_str = date.today().strftime("%d/%m/%y")
    row_index = first_index

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
                if skip_not_found is False:
                    print('{:10s}\t{:13s}\t{:10s}\t{:20s}\t{}'.format(str(row_index), tracking_code, today_str, '',
                                                                      not_found_str))
                row_index += 1
            else:
                if find_date:
                    location = find_date.string[10:].strip()
                    print('{:10s}\t{:13s}\t{:10s}\t{:20s}\t{}'.format(str(row_index), tracking_code, find_date.group(),
                                                                      location, event_str))
                    row_index += 1
                else:
                    event_str = td.text


def generate_and_print_near_codes(base_code: str, num_above: int, num_below: int, skip_not_found:bool):
    """
        Generates a list of tracking codes that are near a base code in the UPU standard
        format.
    Args:
        base_code (str): Base tracking code that will be used to generate the other codes
        num_above (int): Number of tracking codes "above" the base tracking code
        num_below (int): Number of tracking codes "below" the base tracking code
        skip_not_found (bool): Skip the print of tracking results that are not found
    Returns:
        tracking_code_list (str): String with a list of tracking codes separated with a semicolon
    """

    below_tracking_code_list = []
    above_tracking_code_list = []

    print('{:10s}\t{:13s}\t{:10s}\t{:20s}\t{}'.format('n', 'Código', 'Data', 'Local', 'Evento'))

    base_number = int(base_code[2:10])

    for i in reversed(range(num_below)):
        new_code = base_code[0:2] + str(base_number - (i+1)) + '_' + base_code[-2:]
        new_code_validated = generate_check_digit(tracking_code=new_code)
        below_tracking_code_list.append(new_code_validated)

    web_scrape_tracking_data(tracking_code_list=below_tracking_code_list, skip_not_found=skip_not_found,
                             first_index=-num_above)

    print()
    web_scrape_tracking_data(tracking_code_list=[base_code], skip_not_found=False, first_index=0)
    print()

    for i in range(num_above):
        new_code = base_code[0:2] + str(base_number + (i+1)) + '_' + base_code[-2:]
        new_code_validated = generate_check_digit(tracking_code=new_code)
        above_tracking_code_list.append(new_code_validated)

    web_scrape_tracking_data(tracking_code_list=above_tracking_code_list, skip_not_found=skip_not_found,
                             first_index=1)


def generate_check_digit(tracking_code: str) -> str:
    """
        Generate the check digit of a tracking ode in the UPU standard.
    Args:
        tracking_code (str): Tracking code with 13 digits where the check digit will be replaced with a valid one
    Returns:
        valid_tracking_code (str): tracking_code with the valid check digit
    """
    base_number = int(tracking_code[2:10])

    weights = [8, 6, 4, 2, 3, 5, 9, 7]
    weighted_sum = 0

    for i, digit in enumerate(str(base_number)):
        weighted_sum += weights[i] * int(digit)

    check_digit = 11 - (weighted_sum % 11)
    if check_digit == 10:
        check_digit = 0
    elif check_digit == 11:
        check_digit = 5

    valid_tracking_code = tracking_code.replace('_', str(check_digit))

    return valid_tracking_code


def validate_tracking_code(tracking_code: str) -> bool:
    """
        Validates if a tracking code is in the UPU standard format
    Args:
        tracking_code (str): Tracking code string to be validated

    Returns:
        is_valid (bool): Boolean value indicating if the code is validated
    """
    if len(tracking_code) != 13:
        return False

    if re.match(pattern=r'[A-Za-z]{2}[0-9]{9}[A-Za-z]{2}', string=tracking_code):
        return True
    else:
        return False


def run(base_code: str, num_above: int, num_below: int, skip_not_found: bool):
    """
        Runs application
    Args:
        base_code (str): Base tracking code that will be used to generate the other codes
        num_above (int): Number of tracking codes "above" the base tracking code
        num_below (int): Number of tracking codes "below" the base tracking code
        skip_not_found (bool): Skip the print of tracking results that are not found
    """
    if num_above > 50:
        print('Variável \"num_above\" maior que 50.')
        return
    if num_below > 50:
        print('Variável \"num_below\" maior que 50.')
        return

    if validate_tracking_code(tracking_code=base_code.strip()):
        generate_and_print_near_codes(base_code=base_code.strip(),
                                      num_above=num_above,
                                      num_below=num_below,
                                      skip_not_found=skip_not_found)
    else:
        print(f'Código \"{base_code.strip()}\" inválido, fora do formato AA000000000AA')


if __name__ == '__main__':
    # Código de rastreio aqui no formato AA000000000AA
    base_code = 'AA000000000AA'
    num_above = 50
    num_below = 50
    skip_not_found = True
    run(base_code=base_code, num_above=num_above, num_below=num_below, skip_not_found=skip_not_found)
