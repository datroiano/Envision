from datetime import datetime, timedelta, time
from time import perf_counter
from OptionContractData.OptionClasses.single_contract import SingleOptionsContract
from OptionContractData.UseFunctions.date_time import from_unix_time, to_unix_time
from statistics import mean, stdev


class SingleContractStrategy:
    def __init__(self, ticker, strike, expiration_date, quantity, entry_date, exit_date,
                 entry_exit_period=None, timespan='minute', is_call=True, per_contract_commission=0.00,
                 fill_gaps=True, closed_market_period=(9, 30, 16, 0), pricing_criteria='h',
                 multiplier=1, polygon_api_key='r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz'):
        start_time = perf_counter()

        self.ticker = ticker.upper()
        self.strike = float(strike)
        self.expiration_date = expiration_date
        self.entry_date = entry_date
        self.exit_date = exit_date
        self.timespan = timespan
        self.is_call = is_call
        self.multiplier = multiplier
        self.polygon_api_key = polygon_api_key
        self.entry_exit_period = entry_exit_period if entry_exit_period else ('', '', '', '')  # Maybe change
        self.market_open, self.market_close = (closed_market_period[0:2]), (closed_market_period[2:4])
        self.per_contract_commission = per_contract_commission
        self.quantity = quantity
        self.pricing_criteria = pricing_criteria

        contract = SingleOptionsContract(ticker=self.ticker, strike=self.strike, expiration_date=self.expiration_date,
                                         is_call=self.is_call)
        self.contract_data = contract.get_data(from_date=self.entry_date, to_date=self.exit_date,
                                               window_start_time=self.entry_exit_period[0],
                                               window_end_time=self.entry_exit_period[3],
                                               timespan=self.timespan, multiplier=self.multiplier,
                                               polygon_api_key=self.polygon_api_key)
        self.returned_data_length = len(self.contract_data)
        self.trades_simulated = None

        if fill_gaps:
            self.contract_data = self.fill_data_gaps()
            self.filled_data_length = len(self.contract_data)
        else:
            self.filled_data_length = None

        self.simulation_data = self.run_simulation()
        self.meta_data = self.perform_meta_data()

        end_time = perf_counter()
        self.execution_time = round(end_time - start_time, ndigits=4)

    def input_checker(self):
        pass  # Eventually pass self variables through here before calling API functions (below)

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
        simulation_data = []
        entry_points = [point for point in self.contract_data if
                        to_unix_time(f'{self.entry_date} {self.entry_exit_period[0]}') <= int(point['t']) <=
                        to_unix_time(f'{self.entry_date} {self.entry_exit_period[1]}')]
        exit_points = [point for point in self.contract_data if
                       to_unix_time(f'{self.exit_date} {self.entry_exit_period[2]}') <= int(point['t']) <=
                       to_unix_time(f'{self.exit_date} {self.entry_exit_period[3]}')]
        for entry_point in entry_points:

            entry_time = entry_point['t']
            entry_contract_price = entry_point[self.pricing_criteria]  # CAN TINKER WITH AVERAGES HERE
            entry_strategy_price = entry_contract_price * self.quantity
            entry_volume = entry_point['v']
            entry_volume_weighted = entry_point['vw']
            entry_runs = entry_point['n']

            for exit_point in exit_points:

                exit_time = exit_point['t']
                exit_contract_price = exit_point[self.pricing_criteria]  # CAN TINKER WITH AVERAGES HERE
                exit_strategy_price = exit_contract_price * self.quantity
                exit_volume = exit_point['v']
                exit_volume_weighted = exit_point['vw']
                exit_runs = exit_point['n']

                contract_change_dollars = round(exit_contract_price - entry_contract_price, ndigits=2)
                contract_change_percent = round(contract_change_dollars / entry_contract_price, ndigits=2)
                commission_paid = self.quantity * self.per_contract_commission
                strategy_profit_dollars = round(exit_strategy_price - entry_strategy_price - commission_paid, ndigits=2)
                strategy_profit_percent = round(strategy_profit_dollars / entry_strategy_price, ndigits=2)

                simulated_trade = {'entry_time': entry_time,
                                   'entry_contract_price': entry_contract_price,
                                   'entry_strategy_price': entry_strategy_price,
                                   'entry_volume': entry_volume,
                                   'entry_volume_weighted': entry_volume_weighted,
                                   'entry_runs': entry_runs,
                                   'exit_time': exit_time,
                                   'exit_contract_price': exit_contract_price,
                                   'exit_strategy_price': exit_strategy_price,
                                   'exit_volume': exit_volume,
                                   'exit_volume_weighted': exit_volume_weighted,
                                   'exit_runs': exit_runs,
                                   'contract_change_dollars': contract_change_dollars,
                                   'contract_change_percent': contract_change_percent,
                                   'strategy_profit_dollars': strategy_profit_dollars,
                                   'strategy_profit_percent': strategy_profit_percent
                                   }

                simulation_data.append(simulated_trade)

        self.trades_simulated = len(simulation_data)

        return simulation_data

    def perform_meta_data(self):
        return_percentage_list = [i['contract_change_percent'] for i in self.simulation_data]

        average_contract_change_percent = mean(return_percentage_list)
        average_return_percent = mean(i['strategy_profit_percent'] for i in self.simulation_data)
        standard_deviation_contract_change = stdev(return_percentage_list)
        average_entry_volume = mean([i['entry_volume'] for i in self.simulation_data])
        average_exit_volume = mean([i['exit_volume'] for i in self.simulation_data])
        average_entry_runs = mean([i['entry_runs'] for i in self.simulation_data])
        average_exit_runs = mean([i['exit_runs'] for i in self.simulation_data])
        gap_filled_simulations = len([i for i in self.simulation_data if i['entry_runs'] == 0 or i['exit_runs'] == 0])

        meta_data = {
            "average_contract_change_percent": round(average_contract_change_percent, ndigits=4),
            "standard_deviation_contract_change": round(standard_deviation_contract_change, ndigits=4),
            'average_return_percent': round(average_return_percent, ndigits=4),
            "average_entry_volume": round(average_entry_volume, ndigits=2),
            "average_exit_volume": round(average_exit_volume, ndigits=2),
            "average_entry_runs": round(average_entry_runs, ndigits=2),
            "average_exit_runs": round(average_exit_runs, ndigits=2),
            'total_trades_simulated': self.trades_simulated,
            "auto_filled_trades": gap_filled_simulations
        }

        return meta_data


class TwoOptionStrategy:
    def __init__(self, contract_1, contract_2,
                 entry_date, exit_date, entry_exit_period=None, timespan='minute',
                 per_contract_commission=0.01, fill_gaps=True, closed_market_period=(9, 30, 16, 0), pricing_criteria='h',
                 multiplier=1, polygon_api_key='r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz'):
        start_time = perf_counter()

        self.ticker1, self.strike1, self.expiration_date1, self.quantity1, self.is_call1 = contract_1
        self.ticker2, self.strike2, self.expiration_date2, self.quantity2, self.is_call2 = contract_2
        self.entry_date, self.exit_date = entry_date, exit_date
        self.entry_exit_period = entry_exit_period if entry_exit_period else ('', '', '', '')  # Maybe change
        self.timespan, self.per_contract_commission, self.fill_gaps = timespan, per_contract_commission, fill_gaps
        self.market_open, self.market_close = (closed_market_period[0:2]), (closed_market_period[2:4])
        self.multiplier, self.polygon_api_key, self.pricing_criteria = multiplier, polygon_api_key, pricing_criteria

        contract1 = SingleContractStrategy(ticker=self.ticker1, strike=self.strike1,
                                           expiration_date=self.expiration_date1, quantity=self.quantity1,
                                           entry_date=self.entry_date, exit_date=self.exit_date,
                                           entry_exit_period=self.entry_exit_period, timespan=self.timespan,
                                           is_call=self.is_call1, fill_gaps=self.fill_gaps,
                                           per_contract_commission=self.per_contract_commission,
                                           multiplier=self.multiplier)
        self.contract_data1 = contract1.contract_data
        self.contract_simulation_1 = contract1.simulation_data
        self.contract_meta_data_1 = contract1.meta_data
        self.contract_auto_fills_1 = self.contract_meta_data_1['auto_filled_trades']
        self.contract_execution_time_1 = contract1.execution_time

        contract2 = SingleContractStrategy(ticker=self.ticker2, strike=self.strike2,
                                           expiration_date=self.expiration_date2, quantity=self.quantity2,
                                           entry_date=self.entry_date, exit_date=self.exit_date,
                                           entry_exit_period=self.entry_exit_period, timespan=self.timespan,
                                           is_call=self.is_call2, fill_gaps=self.fill_gaps,
                                           per_contract_commission=self.per_contract_commission,
                                           multiplier=self.multiplier)
        self.contract_data2 = contract2.contract_data
        self.contract_simulation_2 = contract2.simulation_data
        self.contract_execution_time_2 = contract2.execution_time
        self.contract_meta_data_2 = contract2.meta_data
        self.contract_auto_fills_2 = self.contract_meta_data_2['auto_filled_trades']

        self.combined_simulation_data = self.run_dual_simulation()

        self.meta_data = self.perform_meta_analysis()

        end_time = perf_counter()
        self.execution_time = round(end_time - start_time, ndigits=4)

    def run_dual_simulation(self):
        simulation_data = []

        for point1, point2 in zip(self.contract_simulation_1, self.contract_simulation_2):
            entry_contract_value = point1['entry_contract_price'] + point2['entry_contract_price']
            entry_strategy_value = point1['entry_strategy_price'] + point2['entry_strategy_price']
            exit_contract_value = point1['exit_contract_price'] + point2['exit_contract_price']
            exit_strategy_value = point1['exit_strategy_price'] + point2['exit_strategy_price']
            contract_dollar_change = round(exit_contract_value - entry_contract_value, ndigits=2)
            contract_percent_change = round(contract_dollar_change / entry_contract_value, ndigits=2)
            strategy_dollar_change = round(exit_strategy_value - entry_strategy_value, ndigits=2)
            strategy_profit_percent = round(strategy_dollar_change / exit_strategy_value, ndigits=2)

            combined_trade = {'entry_time': point1['entry_time'],
                              'exit_time': point1['exit_time'],
                              'entry_contract_value': entry_contract_value,
                              'entry_strategy_value': entry_strategy_value,
                              'exit_contract_value': exit_contract_value,
                              'exit_strategy_value': exit_strategy_value,
                              'contract_dollar_change': contract_dollar_change,
                              'contract_percent_change': contract_percent_change,
                              'strategy_dollar_change': strategy_dollar_change,
                              'strategy_profit_percent': strategy_profit_percent,
                              'entry_volume': point1['entry_volume'] + point2['entry_volume'],
                              'entry_runs': point1['entry_runs'] + point2['entry_runs'],
                              'exit_volume': point1['exit_volume'] + point2['exit_volume'],
                              'exit_runs': point1['exit_runs'] + point2['exit_runs'],
                              }

            simulation_data.append(combined_trade)

        return simulation_data

    def perform_meta_analysis(self):
        average_contract_change_percent = mean([i['contract_percent_change'] for i in self.combined_simulation_data])
        std_dev_contract_change = stdev([i['contract_percent_change'] for i in self.combined_simulation_data])
        average_return_percent = mean(i['strategy_profit_percent'] for i in self.combined_simulation_data)
        average_entry_volume = mean(i['entry_volume'] for i in self.combined_simulation_data)
        average_exit_volume = mean(i['exit_volume'] for i in self.combined_simulation_data)
        average_entry_runs = mean(i['entry_runs'] for i in self.combined_simulation_data)
        average_exit_runs = mean(i['exit_runs'] for i in self.combined_simulation_data)
        auto_filled_trades = self.contract_auto_fills_1 + self.contract_auto_fills_2

        meta_data = {
            "average_contract_change_percent": round(average_contract_change_percent, ndigits=4),
            "standard_deviation_contract_change": round(std_dev_contract_change, ndigits=4),
            'average_return_percent': round(average_return_percent, ndigits=4),
            "average_entry_volume": round(average_entry_volume, ndigits=2),
            "average_exit_volume": round(average_exit_volume, ndigits=2),
            "average_entry_runs": round(average_entry_runs, ndigits=2),
            "average_exit_runs": round(average_exit_runs, ndigits=2),
            'total_trades_simulated': len(self.combined_simulation_data),
            "auto_filled_trades": auto_filled_trades,
            'contract_1_meta_data': self.contract_meta_data_1,
            'contract_2_meta_data': self.contract_meta_data_2,
        }

        return meta_data







