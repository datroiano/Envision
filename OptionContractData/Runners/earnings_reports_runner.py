from OptionContractData.EarningsClasses.earnings_reports import EarningsCompanies

test = EarningsCompanies(from_date='2023-11-12', to_date='2024-02-21')
print(test.raw_data)

print(f'\nExecution time: {test.execution_time:.4f} seconds')
