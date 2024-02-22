import requests
from time import perf_counter


class EarningsCompanies:
    def __init__(self, from_date, to_date, report_time='any', min_eps=None, max_eps=None, real_rev_min=None,
                 real_rev_max=None, est_rev_min=None, est_rev_max=None, allow_nones=True, remove_empties=False,
                 api_key='sS3gwZ7cycpxe9G7JSAmwigdeOjvN2B4'):
        start_time = perf_counter()

        self.from_date = from_date
        self.to_date = to_date
        self.min_eps = min_eps
        self.max_eps = max_eps
        self.report_time = report_time
        self.real_rev_min = real_rev_min
        self.real_rev_max = real_rev_max
        self.est_rev_min = est_rev_min
        self.est_rev_max = est_rev_max
        self.api_key = api_key
        self.remove_empties = remove_empties
        self.allow_nones = allow_nones

        self.raw_data = self.get_raw_data()
        self.cleaned_data = self.clean_data()
        self.filtered_data = self.filter_data()

        end_time = perf_counter()
        self.execution_time = end_time - start_time

    def get_raw_data(self):
        url = f"https://financialmodelingprep.com/api/v3/earning_calendar?from={self.from_date}&to={self.to_date}&apikey={self.api_key}"
        response = requests.get(url)

        if response.status_code == 401:
            print("Unauthorized access. Check your API key.")
            return None

        return response.json()

    def clean_data(self):
        clean_data = [i for i in self.raw_data if
                      {'date', 'symbol', 'time', 'eps', 'revenueEstimated', 'revenue'}.issubset(
                          i.keys()) and '.' not in i.get('symbol', '') and (
                              not self.remove_empties or all(v is not None for v in i.values()))]

        return clean_data

    def filter_data(self):
        return [item for item in self.cleaned_data if
                (self.report_time == 'any' or item['time'] == self.report_time) and
                (self.min_eps is None or item.get('eps') is not None and self.min_eps <= item[
                    'eps'] <= self.max_eps) and
                (self.allow_nones or (item['revenue'] is not None and
                                      self.real_rev_min <= item['revenue'] <= self.real_rev_max)) and
                (self.allow_nones or (item['revenueEstimated'] is not None and
                                      self.est_rev_min <= item['revenueEstimated'] <= self.est_rev_max))]

    def get_specific_company(self, ticker):
        return [i for i in self.filtered_data if i['symbol'] == ticker.upper()]


test = EarningsCompanies(from_date='2023-11-12', to_date='2024-02-21')
print(test.raw_data)

print(f'\nExecution time: {test.execution_time} seconds')
