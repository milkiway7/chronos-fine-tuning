from abc import ABC, abstractmethod
import pandas as pd

from constants import CONSTANTS_GLOBAL
class data_processor_base(ABC):
    def __init__(self,repository,bath_size = 50000):
        self.batch_size = bath_size
        self.repository = repository
        self.symbols = CONSTANTS_GLOBAL["symbol"]
        self.intervals = CONSTANTS_GLOBAL["interval"]

    @abstractmethod
    async def process_data(self):
        pass

    def to_dataframe(self, data):
        data_list = []
        for item in data:
            item_dict = item.__dict__.copy()  
            item_dict.pop('_sa_instance_state', None)  
            data_list.append(item_dict)
        return pd.DataFrame(data_list)
    
    def transform_data(self, df):
        # add columns to indicate symbol and interval
        columns_not_to_round = []

        for symbol_name in self.symbols:
            for interval_name in self.intervals:
                df[symbol_name + "_" + interval_name] = 0
                column_name = symbol_name + "_" + interval_name
                df.loc[(df["Symbol"] == symbol_name) & (df["Interval"] == interval_name), column_name] = 1
                columns_not_to_round.append(column_name)

        columns_to_round = [col for col in df.columns if col not in columns_not_to_round]
        df[columns_to_round] = df[columns_to_round].round(4)
        df.drop(columns = ["CloseTime", "OpenTime","Id","Symbol","Interval"], inplace=True)   
        return df  



        
        
        


