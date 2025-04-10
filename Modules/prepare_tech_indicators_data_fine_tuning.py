import os
import pandas as pd
import logging
from Database.Repositories.tech_indicators_repository import technical_indicators_repository

INTERVALS = ["1m", "5m", "15m","1h","4h","1d"]

class tech_indicators_data_processor:
    def __init__(self,output_path = "data/parquet/technical_indicators"):
        self.repository = technical_indicators_repository()
        self.output_path = output_path
        os.makedirs(self.output_path, exist_ok=True)

    async def process_data(self):
        for interval in INTERVALS:
            indicators = await self.repository.get_tech_indicators_by_interval(interval)
            df = self.to_dataframe(indicators)
            timestamp = df["CloseTime"].iloc[-1]
            df = self.transform_data(df)
            self.save_to_parquet(df, interval, timestamp)

    def to_dataframe(self, indicators):
        indicators_list = []
        for indicator in indicators:
            indicator_dict = indicator.__dict__.copy()
            indicator_dict.pop('_sa_instance_state', None)
            indicators_list.append(indicator_dict)
        return pd.DataFrame(indicators_list)

    def transform_data(self, df):
        df["DateTime"] = pd.to_datetime(df["CloseTime"], unit="ms")
        df["DateTime"] = df["DateTime"].dt.floor('T')

        df.drop(columns=["CloseTime", "Id"], inplace=True)

        df["Value"] = df["Value"].apply(pd.to_numeric, errors='coerce')
        df["Value"] = df["Value"].round(4)

        columns_to_string = ["Symbol", "Interval","Indicator"]
        df[columns_to_string] = df[columns_to_string].astype('string')
        return df
    
    def save_to_parquet(self, df, interval, timestamp):
        file_name = f"{interval}-{timestamp}.parquet"
        file_path = os.path.join(self.output_path, file_name)
        df.to_parquet(file_path, index=False)
        logging.info(f"Saved {len(df)} technical indicators data to {file_path}")