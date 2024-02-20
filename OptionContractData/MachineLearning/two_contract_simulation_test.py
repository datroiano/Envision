from OptionContractData.OptionClasses.multiple_strategy_simulation import MultipleStrategySimulation
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

ticker1 = 'CSCO'
strike1 = 50
expiration_date1 = '2024-02-16'
quantity1 = 1
is_call_1 = True
contract_1 = (ticker1, strike1, expiration_date1, quantity1, is_call_1)

ticker2 = 'CSCO'
strike2 = 50
expiration_date2 = '2024-02-16'
quantity2 = 1
is_call_2 = False
contract_2 = (ticker2, strike2, expiration_date2, quantity2, is_call_2)

ex_input1 = (2, contract_1, contract_2,
             '2024-02-15', '2024-02-15', ('10:30:00', '11:30:00', '15:30:00', '16:00:00'), 'minute',
             0.01, True, (9, 30, 16, 0), 'c',
             1, 'r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz')

ex_input2 = (2, contract_1, contract_2,
             '2024-02-14', '2024-02-14', ('10:30:00', '11:30:00', '15:30:00', '16:00:00'), 'minute',
             0.01, True, (9, 30, 16, 0), 'c',
             1, 'r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz')

ex_input3 = (2, contract_1, contract_2,
             '2024-02-13', '2024-02-13', ('10:30:00', '11:30:00', '15:30:00', '16:00:00'), 'minute',
             0.01, True, (9, 30, 16, 0), 'c',
             1, 'r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz')

test = MultipleStrategySimulation(simulation_list=[ex_input1, ex_input2, ex_input3], create_fluid_model=True)

df = pd.DataFrame(test.fluid_model)

df['entry_time'] = pd.to_datetime(df['entry_time'], unit='ms')
df['exit_time'] = pd.to_datetime(df['exit_time'], unit='ms')

# Extract features from entry and exit time
df['entry_hour'] = df['entry_time'].dt.hour
df['entry_minute'] = df['entry_time'].dt.minute
df['entry_dayofweek'] = df['entry_time'].dt.dayofweek

df['exit_hour'] = df['exit_time'].dt.hour
df['exit_minute'] = df['exit_time'].dt.minute
df['exit_dayofweek'] = df['exit_time'].dt.dayofweek

# Selecting independent and dependent variables
independent_vars = ['entry_hour', 'entry_minute', 'entry_dayofweek', 'exit_hour', 'exit_minute', 'exit_dayofweek',
                    'exit_volume']
dependent_var = 'strategy_profit_percent'

# Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df[independent_vars], df[dependent_var], test_size=0.2, random_state=42)

# Creating and fitting the linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Making predictions
y_pred = model.predict(X_test)

# Model evaluation
print('Coefficients:', [f'{coeff:.6f}' for coeff in model.coef_])
print('Mean squared error:', f'{mean_squared_error(y_test, y_pred):.6f}')
print('Coefficient of determination (R^2):', r2_score(y_test, y_pred))
