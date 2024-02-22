import requests


class ContractSpread:
    def __init__(self, underlying, expiration_date_gte, date_as_of, is_call=None, current_underlying=None,
                 expired=False, call_limit=10, polygon_api_key='r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz'):
        self.underlying, self.expiration_date_gte, self.date_as_of = underlying.upper(), expiration_date_gte, date_as_of
        self.is_call = None if is_call is None else 'call' if is_call else 'put'
        self.current_underlying = current_underlying
        self.strike_price_min, self.strike_price_max = (None, None) if current_underlying is None else \
            (current_underlying - 5, current_underlying + 5)
        self.expired, self.call_limit, self.polygon_api_key = expired, call_limit, polygon_api_key

        self.contracts_data = self.get_options_contracts()
        self.best_matches = self.get_best_matched_contracts()

    def get_options_contracts(self):
        params = {
            'underlying_ticker': self.underlying,
            'contract_type': self.is_call,
            'expiration_date.gte': self.expiration_date_gte,
            'as_of': self.date_as_of,
            'strike_price.gte': self.strike_price_min,
            'strike_price.lte': self.strike_price_max,
            'expired': self.expired,
            'limit': self.call_limit,
            'apiKey': self.polygon_api_key
        }

        endpoint = 'https://api.polygon.io/v3/reference/options/contracts'

        response = requests.get(endpoint, params=params).json()

        return response['results']

    def get_best_matched_contracts(self):
        strikes = [i['strike_price'] for i in self.contracts_data]
        nearest_num = min(strikes, key=lambda x: abs(x - self.current_underlying))
        return [i for i in self.contracts_data if i['strike_price'] == nearest_num]

# test = ContractSpread(underlying='aapl', expiration_date_gte='2024-02-08', date_as_of='2024-02-08', current_underlying=180,
#                       is_call=True)
