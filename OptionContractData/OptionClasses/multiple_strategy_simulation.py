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

                simulation_data.append(double_strategy.combined_simulation_data)
                simulation_meta_data.append(double_strategy.meta_data)

        return simulation_data[0], simulation_meta_data

    def merge_data(self):
        fluid_model = []
        for trade in self.simulation_trade_data:
            fluid_model.append(trade)
        return fluid_model



