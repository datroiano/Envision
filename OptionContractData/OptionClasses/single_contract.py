from OptionContractData.UseFunctions.date_time import to_unix_time
from OptionContractData.UseFunctions.entries import create_options_ticker
import requests


class SingleOptionsContract:
    def __init__(self, ticker: str, strike: float, expiration_date: str, is_call: bool) -> None:
        self.ticker = str(ticker).upper()
        self.strike = float(strike)
        self.expiration_date, self.is_call = expiration_date, is_call

    def get_data(self, from_date: str, to_date: str, window_start_time: str, window_end_time: str, timespan: str,
                 multiplier: int = 1, polygon_api_key: str = 'r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz') -> list[dict] or None:
        from_date = to_unix_time(f'{from_date} {window_start_time}')
        to_date = to_unix_time(f'{to_date} {window_end_time}')

        options_ticker = create_options_ticker(ticker=self.ticker,
                                               strike=self.strike,
                                               expiration_date=self.expiration_date,
                                               contract_type=self.is_call)

        headers = {"Authorization": f"Bearer {polygon_api_key}"}

        endpoint = f"https://api.polygon.io/v2/aggs/ticker/{options_ticker}/range/{multiplier}/{timespan}/{from_date}/{to_date}"

        response = requests.get(endpoint, headers=headers).json()

        if response.get('queryCount', 0) == 0 or response.get('status') == 'ERROR':
            return None
        else:
            return response['results']

# test_contract = SingleOptionsContract("aapl", 160, '2024-02-16', True)
# test_contract_data = test_contract.get_data(from_date='2024-02-11', to_date='2024-02-12',
#                                             window_start_time='09:30:00', window_end_time='16:30:00',
#                                             timespan='minute')
