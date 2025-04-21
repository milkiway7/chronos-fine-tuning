import pandas as pd
import os
import logging
from Modules.BaseClass.data_processor_base import data_processor_base

class candle_data_processor(data_processor_base):
    def __init__(self,repository, batch_size = 50000):
        super().__init__(repository, batch_size)

    async def process_data(self):
        for interval in self.intervals:
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
                df_parts = pd.concat(df_parts, ignore_index=True)
                yield df_parts
                df_parts.clear()
                