from datetime import datetime, timedelta, time
from OptionContractData.OptionClasses.single_contract import SingleOptionsContract
from OptionContractData.UseFunctions.date_time import from_unix_time


class SingleContractStrategy:
    def __init__(self, ticker, strike, expiration_date, quantity, entry_date, exit_date,
                 entry_exit_period=None, timespan='minute', is_call=True, per_contract_commission=0,
                 fill_gaps=True, closed_market_period=(9, 30, 16, 0),
                 multiplier=1, polygon_api_key='r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz'):
        self.ticker = ticker.upper()
        self.strike = float(strike)
        self.expiration_date = expiration_date
        self.entry_date = entry_date
        self.exit_date = exit_date
        self.timespan = timespan
        self.is_call = is_call
        self.multiplier = multiplier
        self.polygon_api_key = polygon_api_key
        self.entry_exit_period = entry_exit_period if entry_exit_period else ('', '', '', '')  # Just reference using indexes
        self.market_open, self.market_close = (closed_market_period[0:2]), (closed_market_period[2:4])
        self.per_contract_commission = per_contract_commission

        contract = SingleOptionsContract(ticker=self.ticker, strike=self.strike, expiration_date=self.expiration_date)
        self.contract_data = contract.get_data(from_date=self.entry_date, to_date=self.exit_date,
                                               window_start_time=self.entry_exit_period[0],
                                               window_end_time=self.entry_exit_period[3],
                                               timespan=self.timespan, multiplier=self.multiplier,
                                               polygon_api_key=self.polygon_api_key)
        self.returned_data_length = len(self.contract_data)

        if fill_gaps:
            self.contract_data = self.fill_data_gaps()
            self.filled_data_length = len(self.contract_data)
        else:
            self.filled_data_length = None

    def fill_data_gaps(self):

        trading_start_time = time(self.market_open[0], self.market_open[1])
        trading_end_time = time(self.market_close[0], self.market_close[1])

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
            filled_data.append(self.contract_data[i])
            if i < (self.returned_data_length - 1):
                current_time = datetime.fromtimestamp(self.contract_data[i]['t'] / 1000)
                next_time = datetime.fromtimestamp(self.contract_data[i + 1]['t'] / 1000)
                while current_time + interval < next_time and (
                        trading_start_time <= current_time.time() <= trading_end_time):
                    current_time += interval
                    filled_data.append({
                        'v': self.contract_data[i]['v'],
                        'vw': self.contract_data[i]['vw'],
                        'o': self.contract_data[i]['c'],  # assuming the open is equal to the previous close
                        'c': self.contract_data[i]['c'],
                        'h': self.contract_data[i]['c'],
                        'l': self.contract_data[i]['c'],
                        't': int(current_time.timestamp() * 1000),
                        'n': 0  # fill gap indicator
                    })
        return filled_data

    def run_simulation(self):
        pass


test = SingleContractStrategy('aapl', 190, (24, 2, 16), 1, '2024-02-14',
                              '2024-02-15', entry_exit_period=('09:30:00', '10:00:00', '', '14:30:00'),
                              timespan='minute', is_call=True, fill_gaps=True)
for item in test.contract_data:
    print(from_unix_time(item['t']))
print(test.returned_data_length)
print(test.filled_data_length)
