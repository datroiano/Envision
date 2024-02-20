from OptionContractData.OptionClasses.option_strategies import TwoOptionStrategy

ticker1 = 'AAPL'
strike1 = 185
expiration_date1 = (24, 2, 23)
quantity1 = 2
is_call_1 = True
contract_1 = (ticker1, strike1, expiration_date1, quantity1, is_call_1)

ticker2 = 'AAPL'
strike2 = 185
expiration_date2 = (24, 2, 23)
quantity2 = 2
is_call_2 = False
contract_2 = (ticker2, strike2, expiration_date2, quantity2, is_call_2)

test = TwoOptionStrategy(contract_1=contract_1,
                         contract_2=contract_2,
                         entry_date='2024-02-15',
                         exit_date='2024-02-15',
                         entry_exit_period=('09:30:00', '10:30:00', '14:30:00', '16:00:00'),
                         closed_market_period=(9, 30, 16, 0),
                         pricing_criteria='h',
                         per_contract_commission=0.06,
                         fill_gaps=True,
                         timespan='minute',
                         multiplier=1,
                         polygon_api_key='r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz')

print(f'{test.meta_data}\n')
print(f'Average Return Percent: {test.meta_data["average_return_percent"] * 100:.2f}%')
print(f'Average Dollar Change: {test.meta_data["average_contract_change_percent"] * 100:.2f}%')
print(f'Execution time: {test.execution_time} sec')
print(f'Execution time, contract 1: {test.contract_execution_time_1} sec')
print(f'Execution time, contract 2: {test.contract_execution_time_2} sec')
