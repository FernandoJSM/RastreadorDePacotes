
def generate_near_codes(base_code: str, num_above: int, num_below: int) -> str:
    """
        Generates a list of tracking codes that are near a base code in the UPU standard
        format.
    Args:
        base_code (str): Base tracking code that will be used to generate the other codes
        num_above (int): Number of tracking codes "above" the base tracking code
        num_below (int): Number of tracking codes "below" the base tracking code
    Returns:
        code_list (str): String with a list of tracking codes separated with a semicolon
    """

    code_list = ''

    return code_list


def get_and_print_tracking_results(code_list: str):
    """
        Get a code list and retrieves the results
    Args:
        code_list (str): String with a list of tracking codes separated with a semicolon
    """

    pass


def run(base_code: str, num_above: int, num_below: int):
    """
        Runs application
    Args:
        base_code (str): Base tracking code that will be used to generate the other codes
        num_above (int): Number of tracking codes "above" the base tracking code
        num_below (int): Number of tracking codes "below" the base tracking code
    """
    code_list = generate_near_codes(base_code=base_code, num_above=num_above, num_below=num_below)
    get_and_print_tracking_results(code_list=code_list)


if __name__ == '__main__':
    # Código de rastreio aqui no formato AA000000000AA
    base_code = 'AA000000000AA'
    num_above = 20
    num_below = 20
    run(base_code=base_code, num_above=num_above, num_below=num_below)

