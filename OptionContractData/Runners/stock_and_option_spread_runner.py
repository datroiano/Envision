from OptionContractData.StockClasses.single_stock import SingleStock
from OptionContractData.OptionClasses.existing_contracts_for_underlying import ContractSpread

test_instance_stock = SingleStock(ticker='aapl',
                                  from_date='2024-02-21',
                                  from_time='09:30:00',
                                  to_date='2024-02-21',
                                  to_time='10:30:00',
                                  fill_gaps=True)

test_instance_contracts = ContractSpread(underlying=test_instance_stock.ticker,
                                         expiration_date_gte=test_instance_stock.from_date,
                                         date_as_of=test_instance_stock.from_date,
                                         current_underlying=test_instance_stock.get_average_price(),
                                         is_call=True,
                                         call_limit=10)

print(test_instance_contracts.best_matches)