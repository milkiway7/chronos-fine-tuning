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
        columns_not_to_round = ["Symbol", "Interval","Year", "Month", "Day", "Hour", "Minute"]
        # chage timestamp to yyyy-mm-dd format and separate it into year, month, day, hour, minute
        self.transform_timestamp(df)
        df.drop(columns = ["CloseTime", "OpenTime","Id"], inplace=True)   
        columns_to_round = [col for col in df.columns if col not in columns_not_to_round]
        for col in columns_to_round:
            df[col] = pd.to_numeric(df[col], errors='coerce') 
            df[columns_to_round] = df[columns_to_round].round(4)
        print(df.head())
        return df  

    def transform_timestamp(self,df):
        df["CloseTime"] = pd.to_datetime(df["CloseTime"], unit='ms')
        df["Year"] = df["CloseTime"].dt.year
        df["Month"] = df["CloseTime"].dt.month
        df["Day"] = df["CloseTime"].dt.day
        df["Hour"] = df["CloseTime"].dt.hour
        df["Minute"] = df["CloseTime"].dt.minute