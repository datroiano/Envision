from OptionContractData.EarningsClasses.earnings_reports import EarningsCompanies
from OptionContractData.StockClasses.single_stock import SingleStock
from OptionContractData.UseFunctions.date_time import previous_day
from OptionContractData.OptionClasses.existing_contracts_for_underlying import ContractSpread
from OptionContractData.OptionClasses.multiple_strategy_simulation import MultipleStrategySimulation
from time import perf_counter


class MasterEarningsSimulation:
    def __init__(self, entry_period_start, entry_period_end, exit_period_start, exit_period_end,
                 earnings_date_s, earnings_date_e, earnings_report_time, max_companies=10, timespan='minute',
                 multiplier=1, pricing_criteria='h', attempts_per_company=1, contract_quantity=1,
                 roundtrip_commission=0.02,
                 min_eps=None, max_eps=None, real_rev_min=None, real_rev_max=None, est_rev_min=None, est_rev_max=None,
                 allow_nones=True, remove_empties=False, polygon_api_key='r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz'):
        start_time = perf_counter()

        self.entry_s, self.entry_e = entry_period_start, entry_period_end
        self.exit_s, self.exit_e = exit_period_start, exit_period_end
        self.earnings_dates_s, self.earnings_dates_e = earnings_date_s, earnings_date_e
        self.earnings_report_time, self.timespan, self.multiplier = earnings_report_time, timespan, multiplier
        self.min_eps, self.max_eps, self.real_rev_min, self.real_rev_max = min_eps, max_eps, real_rev_min, real_rev_max
        self.est_rev_min, self.est_rev_max, self.allow_nones = est_rev_min, est_rev_max, allow_nones
        self.remove_empties, self.max_companies, self.pricing_criteria = remove_empties, max_companies, pricing_criteria
        self.attempts_per_company, self.contract_quantity = attempts_per_company, contract_quantity
        self.roundtrip_commission, self.polygon_api_key = roundtrip_commission, polygon_api_key
        self.stock_errors, self.contract_spread_errors, self.entry_count, self.contract_errors = 0, 0, 0, 0

        self.input_companies_from_cal = self.get_companies_from_earnings_calendar()
        self.option_inputs_raw = self.get_simulation_inputs_raw()
        self.master_simulations_final_inputs = self.create_multiple_simulation_entry()

        self.simulation_trade_data, self.simulation_meta_data, self.fluid_model = [], [], []
        self.run_bulk_simulation()

        end_time = perf_counter()
        self.execution_time = end_time - start_time

    def get_companies_from_earnings_calendar(self):
        earnings_cal = EarningsCompanies(from_date=self.earnings_dates_s,
                                         to_date=self.earnings_dates_e,
                                         min_eps=self.min_eps,
                                         max_eps=self.max_eps,
                                         real_rev_min=self.real_rev_min,
                                         real_rev_max=self.real_rev_max,
                                         est_rev_min=self.est_rev_min,
                                         est_rev_max=self.est_rev_max,
                                         allow_nones=self.allow_nones,
                                         remove_empties=self.remove_empties)

        clean_calendar = [i for i in earnings_cal.filtered_data if
                          all(char not in i['symbol'] for char in ['+', '.', '-'])]

        input_companies_from_cal = clean_calendar[0:self.max_companies + 10]

        return input_companies_from_cal

    def get_simulation_inputs_raw(self):
        full_simulation_input = []
        for company in self.input_companies_from_cal:
            if self.entry_count >= self.max_companies:
                break
            try:
                from_date = previous_day(company['date']) if company['time'] == 'bmo' else company['date']

                company_stock = SingleStock(ticker=company['symbol'],
                                            from_date=from_date,
                                            from_time=self.entry_s,
                                            to_date=from_date,
                                            to_time=self.entry_e,
                                            timespan=self.timespan,
                                            multiplier=self.multiplier)

                contract_spread = ContractSpread(underlying=company['symbol'], expiration_date_gte=from_date,
                                                 date_as_of=from_date, is_call=True,
                                                 current_underlying=company_stock.get_average_price(),
                                                 call_limit=10)

                # print(f'{i} Company {company["symbol"]} is {company_stock.get_average_price():.2f}')

                added_count = 0
                for _ in range(self.attempts_per_company):
                    for contract_info in contract_spread.best_matches:
                        if added_count >= self.attempts_per_company:
                            break
                        test_conditions = {
                            'ticker': company['symbol'],
                            'strike_price': contract_info['strike_price'],
                            'trade_date': from_date,
                            'expiration_date_target': contract_info['expiration_date'],
                        }
                        full_simulation_input.append(test_conditions)
                        added_count += 1
                    if added_count >= self.attempts_per_company:
                        break

                self.entry_count += 1
            except TypeError:
                self.stock_errors += 1
                continue
            except ValueError:
                self.contract_spread_errors += 1
                continue
        # print(full_simulation_input)
        # print(f'Stock Errors: {stock_errors}')
        # print(f'Option Errors: {contract_spread_errors}')

        return full_simulation_input

    def create_multiple_simulation_entry(self):
        master_entry = []
        for entry in self.option_inputs_raw:
            ticker = entry['ticker']
            strike = entry['strike_price']
            expiration_date = entry['expiration_date_target']
            contract1 = (ticker, strike, expiration_date, self.contract_quantity, True)
            contract2 = (ticker, strike, expiration_date, self.contract_quantity, False)
            trade_date = entry['trade_date']

            iteration_bound_test = (2, contract1, contract2, trade_date, trade_date,
                                    (self.entry_s, self.entry_e, self.exit_s, self.exit_e),
                                    self.timespan,
                                    self.roundtrip_commission, True, (9, 30, 16, 0), self.pricing_criteria,
                                    self.multiplier, self.polygon_api_key)

            master_entry.append(iteration_bound_test)

        return master_entry

    def run_bulk_simulation(self):
        bulk_simulation = MultipleStrategySimulation(simulation_list=self.master_simulations_final_inputs,
                                                     create_fluid_model=True)
        self.simulation_trade_data = bulk_simulation.simulation_trade_data
        self.simulation_meta_data = bulk_simulation.simulation_meta_data
        self.fluid_model = bulk_simulation.fluid_model


    def check_rebound_data(self):
        if len(self.simulation_meta_data) < self.max_companies:
            self.contract_errors += len(self.simulation_meta_data) < self.max_companies

    def add_missing_data(self):



test = MasterEarningsSimulation(entry_period_start='09:30:00', entry_period_end='10:30:00',
                                exit_period_start='14:30:00',
                                exit_period_end='16:00:00', earnings_date_s='2024-02-15', earnings_date_e='2024-02-21',
                                earnings_report_time='any', max_companies=3, timespan='minute',
                                multiplier=1, pricing_criteria='h',
                                min_eps=None, max_eps=None, real_rev_min=None, real_rev_max=None,
                                est_rev_min=None,
                                est_rev_max=None, attempts_per_company=1,
                                allow_nones=True, remove_empties=False)

print(test.check_rebound_data())
print(f'Execution time: {test.execution_time} seconds')
