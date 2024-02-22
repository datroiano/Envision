from OptionContractData.EarningsClasses.earnings_reports import EarningsCompanies
from OptionContractData.StockClasses.single_stock import SingleStock


class MasterEarningsSimulation:
    def __init__(self, entry_period_start, entry_period_end, exit_period_start, exit_period_end,
                 earnings_date_s, earnings_date_e, earnings_report_time, max_companies=10, timespan='minute',
                 multiplier=1, pricing_criteria='h',
                 min_eps=None, max_eps=None, real_rev_min=None, real_rev_max=None, est_rev_min=None, est_rev_max=None,
                 allow_nones=True, remove_empties=False):
        self.entry_s, self.entry_e = entry_period_start, entry_period_end
        self.exit_s, self.exit_e = exit_period_start, exit_period_end
        self.earnings_dates_s, self.earnings_dates_e = earnings_date_s, earnings_date_e
        self.earnings_report_time, self.timespan, self.multiplier = earnings_report_time, timespan, multiplier
        self.min_eps, self.max_eps, self.real_rev_min, self.real_rev_max = min_eps, max_eps, real_rev_min, real_rev_max
        self.est_rev_min, self.est_rev_max, self.allow_nones = est_rev_min, est_rev_max, allow_nones
        self.remove_empties, self.max_companies, self.pricing_criteria = remove_empties, max_companies, pricing_criteria

    def get_inputs_from_earnings_calendar(self):
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

        earnings_inputs = earnings_cal.get_input_list_option_strategy(
            entry_start=self.entry_s,
            entry_end=self.entry_e,
            timespan=self.timespan,
            multiplier=self.multiplier)

        earnings_inputs = [item for item in earnings_inputs if '+' not in item['ticker']]
        # Any additional cleaning criteria
        earnings_inputs = earnings_inputs[0:(self.max_companies + 1)]

        # for stock in earnings_inputs:
        #     stock_obj = SingleStock(ticker=stock['ticker'],
        #                             from_date=stock['from_date'],
        #                             to_date=stock['to_date'],
        #                             from_time=stock['from_time'],
        #                             to_time=stock['to_time'])
        # print(stock_obj.stock_data)

        return earnings_inputs


test = MasterEarningsSimulation(entry_period_start='09:30:00', entry_period_end='10:30:00',
                                exit_period_start='14:30:00', exit_period_end='16:00:00',
                                earnings_date_s='2024-02-10', earnings_date_e='2024-02-20',
                                earnings_report_time='any')

print(test.get_inputs_from_earnings_calendar())

entry = {'ticker': 'ALX', 'from_date': '2024-02-11', 'to_date': '2024-02-11', 'from_time': '09:30:00',
         'to_time': '10:30:00', 'fill_gaps': True, 'timespan': 'minute', 'multiplier': 1}, {'ticker': 'TORO',
                                                                                            'from_date': '2024-02-11',
                                                                                            'to_date': '2024-02-11',
                                                                                            'from_time': '09:30:00',
                                                                                            'to_time': '10:30:00',
                                                                                            'fill_gaps': True,
                                                                                            'timespan': 'minute',
                                                                                            'multiplier': 1}
