import statistics

from OptionContractData.OptionClasses.option_strategies import SingleContractStrategy, TwoOptionStrategy
from time import perf_counter


class MultipleStrategySimulation:
    def __init__(self, simulation_list, create_fluid_model=False):
        start_time = perf_counter()

        self.simulation_list = simulation_list
        self.simulation_trade_data, self.simulation_meta_data = self.run_simulations()

        if create_fluid_model:
            self.fluid_model = self.merge_data()

        end_time = perf_counter()
        self.execution_time = end_time - start_time

    def run_simulations(self):
        simulation_data = []
        simulation_meta_data = []
        for entry in self.simulation_list:
            try:
                if entry[0] == 1:
                    single_strategy = SingleContractStrategy(ticker=entry[1],
                                                             strike=entry[2],
                                                             expiration_date=entry[3],
                                                             quantity=entry[4],
                                                             entry_date=entry[5],
                                                             exit_date=entry[6],
                                                             entry_exit_period=entry[7],
                                                             timespan=entry[8],
                                                             per_contract_commission=entry[9],
                                                             fill_gaps=entry[10],
                                                             closed_market_period=entry[11],
                                                             pricing_criteria=entry[12],
                                                             multiplier=entry[13],
                                                             polygon_api_key=entry[14],
                                                             )
                    simulation_data.append(single_strategy.simulation_data)
                    simulation_meta_data.append(single_strategy.meta_data)
                elif entry[0] == 2:
                    double_strategy = TwoOptionStrategy(contract_1=entry[1],
                                                        contract_2=entry[2],
                                                        entry_date=entry[3],
                                                        exit_date=entry[4],
                                                        entry_exit_period=entry[5],
                                                        timespan=entry[6],
                                                        per_contract_commission=entry[7],
                                                        fill_gaps=entry[8],
                                                        closed_market_period=entry[9],
                                                        pricing_criteria=entry[10],
                                                        multiplier=entry[11],
                                                        polygon_api_key=entry[12],
                                                        )
                    simulation_data.append({'contract': entry[1],
                                            'simulation': double_strategy.combined_simulation_data})
                    simulation_meta_data.append({'contract': entry[1],
                                                 'meta_data': double_strategy.meta_data})
            except statistics.StatisticsError:
                continue
            except TypeError:
                continue
        try:
            return simulation_data[0], simulation_meta_data
        except IndexError:
            return None, None

    def merge_data(self):
        fluid_model = []
        for run in self.simulation_trade_data:
            print(run)  # Finish this
        return fluid_model

# x = [(2, ('RARE', 45, '2024-02-16', 1, True), ('RARE', 45, '2024-02-16', 1, False), '2024-02-15', '2024-02-15',
#       ('09:30:00', '10:30:00', '14:30:00', '16:00:00'), 'minute', 0.02, True, (9, 30, 16, 0), 'h', 1,
#       'r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz')]
#
# test = MultipleStrategySimulation(simulation_list=x)
# print(test.simulation_trade_data)
