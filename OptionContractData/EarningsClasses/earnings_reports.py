import requests
from time import perf_counter


class EarningsCompanies:
    def __init__(self, from_date, to_date, min_eps=None, max_eps=None, report_time='any', real_rev_min=None,
                 real_rev_max=None, est_rev_min=None, est_rev_max=None, clean_data=True,
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
        self.clean_data = clean_data
        self.api_key = api_key

        self.raw_data = self.get_raw_data()
        self.filtered_data = self.apply_filters()

        end_time = perf_counter()
        self.execution_time = end_time - start_time

    def get_raw_data(self):
        url = f"https://financialmodelingprep.com/api/v3/earning_calendar?from={self.from_date}&to={self.to_date}&apikey={self.api_key}"
        response = requests.get(url)
        return response.json()

    def apply_filters(self):
        filtered_data = []
        for item in self.raw_data:
            if all(key in item for key in
                   ['date', 'symbol', 'eps', 'epsEstimated', 'time', 'revenue', 'revenueEstimated', 'fiscalDateEnding',
                    'updatedFromDate']):
                filtered_item = {key: item[key] for key in item}

                if self.min_eps is not None and filtered_item.get('eps') is not None and filtered_item[
                    'eps'] < self.min_eps:
                    continue
                if self.max_eps is not None and filtered_item.get('eps') is not None and filtered_item[
                    'eps'] > self.max_eps:
                    continue
                if self.report_time != 'any' and filtered_item.get('time') != self.report_time:
                    continue
                if self.real_rev_min is not None and filtered_item.get('revenue') is not None and filtered_item[
                    'revenue'] < self.real_rev_min:
                    continue
                if self.real_rev_max is not None and filtered_item.get('revenue') is not None and filtered_item[
                    'revenue'] > self.real_rev_max:
                    continue
                if self.est_rev_min is not None and filtered_item.get('revenueEstimated') is not None and filtered_item[
                    'revenueEstimated'] < self.est_rev_min:
                    continue
                if self.est_rev_max is not None and filtered_item.get('revenueEstimated') is not None and filtered_item[
                    'revenueEstimated'] > self.est_rev_max:
                    continue

                # If clean_data is True, make all items not equal to None
                if self.clean_data:
                    filtered_item = {k: v for k, v in filtered_item.items() if v is not None}
                    if 'symbol' in filtered_item and '.' in filtered_item['symbol']:
                        continue  # Skip items with '.' in 'symbol'

                filtered_data.append(filtered_item)

        return filtered_data


x = EarningsCompanies(from_date='2023-11-11', to_date='2023-11-14', min_eps=0)
for item in x.filtered_data:
    print(item.get('eps'))

print(f'{x.execution_time} sec')