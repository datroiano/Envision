from OptionContractData.OptionClasses.single_contract import SingleOptionsContract


class SingleContractStrategy:
    def __init__(self, ticker, strike, expiration_date, quantity, entry_date, exit_date,
                 entry_exit_period=None, timespan='minute', is_call=True,
                 fill_gaps=True, multiplier=1, polygon_api_key='r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz'):
        self.ticker = ticker.upper()
        self.strike = float(strike)
        self.expiration_date = expiration_date
        self.entry_date = entry_date
        self.exit_date = exit_date
        self.timespan = timespan
        self.is_call = is_call
        self.multiplier = multiplier
        self.polygon_api_key = polygon_api_key
        self.entry_exit_period = entry_exit_period if entry_exit_period else ('', '', '', '')

        contract = SingleOptionsContract(ticker=self.ticker, strike=self.strike, expiration_date=self.expiration_date)
        self.contract_data = contract.get_data(from_date=self.entry_date, to_date=self.exit_date,
                                               window_start_time=self.entry_exit_period[0],
                                               window_end_time=self.entry_exit_period[1],
                                               timespan=self.timespan, multiplier=self.multiplier,
                                               polygon_api_key=self.polygon_api_key)

    def run_simulation(self):
        pass

test = SingleContractStrategy('aapl', 180, '2024-02-16', 1, '2024-02-14',
                              '2024-02-15', entry_exit_period=('0:', '', '', ''),
                              timespan='minute', is_call=True)
print(test.contract_data)