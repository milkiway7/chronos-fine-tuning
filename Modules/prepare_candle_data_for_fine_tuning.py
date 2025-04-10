import pandas as pd
import os
import logging
from Database.Repositories.candles_repository import candles_repository
# get data order by timestamp ascending with chierarchical structure 1m < 5m < 15m < 30m < 1h < 4h < 1d

INTERVALS = ["1m", "5m", "15m","30m","1h","4h","1d"]


class candle_data_processor:
    def __init__(self, output_path = "data/parquet/candles", batch_size = 50000):
        self.repository = candles_repository()
        self.output_path = output_path
        self.batch_size = batch_size
        os.makedirs(self.output_path, exist_ok=True)

    async def process_data(self):
        for interval in INTERVALS:
            oldest_candle = await self.repository.get_oldest_candle_for_interval(interval)
            start_time = oldest_candle.CloseTime

            df_parts = []

            while True:
                candles = await self.repository.get_candles_by_symbol_timestamp(interval, start_time, self.batch_size)
                if not candles:
                    logging.info(f"No more data for interval {interval}.")
                    break
                
                df = self.to_dataframe(candles)
                df = self.transform_data(df)
                df_parts.append(df)
                
                # Take timestamp from the newest + 1 ms to avoid duplicates
                start_time = candles[-1].CloseTime + 1

            if df_parts:
                full_df = pd.concat(df_parts, ignore_index=True)
                logging.info(f"For interval {interval} - Oldest candle: {full_df["DateTime"].iloc[0]} - Newest candle: {full_df["DateTime"].iloc[-1]}")
                self.save_to_parquet(full_df, interval)  
                df_parts.clear()
                    
    def to_dataframe(self, candles):
        candles_list = []
        for candle in candles:
            candle_dict = candle.__dict__.copy()  # Skopiuj dane obiektu
            candle_dict.pop('_sa_instance_state', None)  # Usuwamy atrybut _sa_instance_state
            candles_list.append(candle_dict)    

        df = pd.DataFrame(candles_list)
        return df
    
    def transform_data(self, df):
        df["DateTime"] = pd.to_datetime(df["CloseTime"], unit="ms")
        df["DateTime"] = df["DateTime"].dt.floor('T')

        df.drop(columns=["CloseTime","Id","OpenTime"], inplace=True)

        columns_to_round = ["Open", "High", "Low", "Close", "Volume"]
        # Przekonwertowanie kolumn na float
        df[columns_to_round] = df[columns_to_round].apply(pd.to_numeric, errors='coerce')
        df[columns_to_round] = df[columns_to_round].round(4)

        # Przekonwertowanie kolumn na string
        columns_to_string = ["Symbol", "Interval"]
        df[columns_to_string] = df[columns_to_string].astype('string')
        return df
    
    def save_to_parquet(self, df, interval):
        file_name = f"{interval}.parquet"
        file_path = os.path.join(self.output_path, file_name)
        df.to_parquet(file_path, index=False)   
        logging.info(f"Saved {len(df)} rows to {file_path}")