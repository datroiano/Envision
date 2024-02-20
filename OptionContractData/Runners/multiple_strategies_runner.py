from OptionContractData.OptionClasses.multiple_strategy_simulation import MultipleStrategySimulation

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

ex_input1 = (2, contract_1, contract_2,
             '2024-02-15', '2024-02-15', ('09:30:00', '10:30:00', '14:30:00', '16:00:00'), 'minute',
             0.01, True, (9, 30, 16, 0), 'h',
             1, 'r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz')

contract = contract_1
ex_input2 = [(1, ticker1, strike1, expiration_date1, quantity1,
              '2024-02-15', '2024-02-15', ('09:30:00', '10:30:00', '14:30:00', '16:00:00'), 'minute',
              0.01, True, (9, 30, 16, 0), 'h',
              1, 'r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz')]

complete_input = [ex_input1, ex_input2]

print(MultipleStrategySimulation(complete_input).simulation_meta_data)
