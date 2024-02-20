import json
from urllib.request import urlopen
import certifi
import ssl


def get_jsonparsed_data(url):
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    with urlopen(url, context=ssl_context) as response:
        data = response.read().decode("utf-8")
    return json.loads(data)


api_key = 'sS3gwZ7cycpxe9G7JSAmwigdeOjvN2B4'
from_date = '2023-11-11'
to_date = '2024-02-15'
url = f"https://financialmodelingprep.com/api/v3/earning_calendar?from={from_date}&to={to_date}&apikey={api_key}"
x = get_jsonparsed_data(url)
for item in x:
    if item['time'] == 'amc' or item['time'] == 'bmo':
        print(item)

print(len(x))

