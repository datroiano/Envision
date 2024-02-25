def create_options_ticker(ticker: str, strike: float, expiration_date: str, contract_type: bool) -> str:
    ticker = str(ticker.upper())
    strike = str(float(strike))
    expiration_year = expiration_date[2:4]
    expiration_month = expiration_date[5:7]
    expiration_day = expiration_date[8:]
    contract_type = 'C' if contract_type else 'P'

    '''
    Strike formatting will look like this:
    1000: 01000000
    1000.5: 01000500
    170.5: 00170500
    '''

    decimal_find = strike.find('.', )
    num_dec = len(strike) - decimal_find - 1
    strike = strike.replace(".", "")

    strike_mapping = {1: {
        1: f'00000{strike}00',
        2: f'0000{strike}00',
        3: f'000{strike}00',
        4: f'00{strike}00',
        5: f'0{strike}00',
        6: f'{strike}00',
    }, 2: {
        1: f'000000{strike}0',
        2: f'00000{strike}0',
        3: f'0000{strike}0',
        4: f'000{strike}0',
        5: f'0{strike}0',
        6: f'{strike}00',
        7: f'{strike}0'
    }
    }

    strike_string_for_insertion = strike_mapping.get(num_dec, '')[len(strike)]

    expiration_month = f'0{expiration_month}' if len(expiration_month) == 1 else expiration_month
    expiration_year = f'0{expiration_year}' if len(expiration_year) == 1 else expiration_year
    expiration_day = f'0{expiration_day}' if len(expiration_day) == 1 else expiration_day

    expiry = f'{expiration_year}{expiration_month}{expiration_day}'

    return f'O:{ticker}{expiry}{contract_type}{strike_string_for_insertion}'
