from OptionContractData.OptionClasses.option_strategies import SingleContractStrategy

test = SingleContractStrategy(ticker='aapl',
                              strike=180,
                              expiration_date='2024-02-16',
                              quantity=1,
                              entry_date='2024-02-14',
                              exit_date='2024-02-14',
                              entry_exit_period=('10:30:00', '11:00:00', '14:30:00', '16:00:00'),
                              timespan='minute',
                              is_call=True,
                              fill_gaps=True,
                              per_contract_commission=0.01,
                              multiplier=1
                              )

print(test.meta_data)
print(test.execution_time)
