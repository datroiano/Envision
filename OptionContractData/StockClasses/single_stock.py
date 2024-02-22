import requests
from OptionContractData.UseFunctions.date_time import to_unix_time, from_unix_time
from datetime import datetime, timedelta, time
from time import perf_counter
from statistics import mean


class SingleStock:
    def __init__(self, ticker, from_date, from_time, to_date, to_time, fill_gaps=True, timespan='minute', multiplier=1,
                 adjusted=False, aggregate_bars_limit=100, polygon_api_key='r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz',
                 closed_market_period=(9, 30, 16, 0), pricing_criteria='h'):
        start_time = perf_counter()

        self.ticker, self.from_date, self.from_time, self.fill_gaps,  = ticker.upper(), from_date, from_time, fill_gaps
        self.to_date, self.to_time, self.timespan, self.polygon_api_key = to_date, to_time, timespan, polygon_api_key
        self.multiplier, self.adjusted, self.aggregate_bars_limit = multiplier, adjusted, aggregate_bars_limit
        self.closed_market_period, self.pricing_criteria = closed_market_period, pricing_criteria

        self.stock_data = self.get_stock_data()

        if self.stock_data is not None: self.returned_data_length = len(self.stock_data)

        if fill_gaps and self.stock_data is not None:
            self.stock_data = self.fill_data_gaps()
            self.filled_data_length = len(self.stock_data)
        else:
            self.filled_data_length = None

        end_time = perf_counter()
        self.execution_time = end_time - start_time

    def get_stock_data(self):
        from_date = to_unix_time(f'{self.from_date} {self.from_time}')
        to_date = to_unix_time(f'{self.to_date} {self.to_time}')
        headers = {"Authorization": f"Bearer {self.polygon_api_key}"}

        endpoint = f"https://api.polygon.io/v2/aggs/ticker/{self.ticker}/range/{self.multiplier}/{self.timespan}/{from_date}/{to_date}"

        response = requests.get(endpoint, headers=headers).json()

        if response.get('queryCount', 0) == 0 or response.get('status') == 'ERROR':
            return None
        else:
            return response['results']

    def fill_data_gaps(self):

        trading_start_time = time(self.closed_market_period[0], self.closed_market_period[1])
        trading_end_time = time(self.closed_market_period[2], self.closed_market_period[3])
        filled_data = []

        time_spans = {
            "minute": timedelta(minutes=1),
            "hour": timedelta(hours=1),
            "day": timedelta(days=1),
            "second": timedelta(seconds=1)
        }
        interval = time_spans.get(self.timespan)

        if interval is None:
            raise ValueError("Invalid timespan specified")

        for i in range(self.returned_data_length):
            filled_data.append(self.stock_data[i])
            if i < (self.returned_data_length - 1):
                current_time = datetime.fromtimestamp(self.stock_data[i]['t'] / 1000)
                next_time = datetime.fromtimestamp(self.stock_data[i + 1]['t'] / 1000)
                while current_time + interval < next_time and (
                        trading_start_time <= current_time.time() <= trading_end_time):
                    current_time += interval
                    filled_data.append({
                        'v': self.stock_data[i]['v'],
                        'vw': self.stock_data[i]['vw'],
                        'o': self.stock_data[i]['c'],  # assuming the open is equal to the previous close
                        'c': self.stock_data[i]['c'],
                        'h': self.stock_data[i]['c'],
                        'l': self.stock_data[i]['c'],
                        't': int(current_time.timestamp() * 1000),
                        'n': 0  # fill gap indicator
                    })
        return filled_data

    def get_average_price(self):
        return mean(i[self.pricing_criteria] for i in self.stock_data)

