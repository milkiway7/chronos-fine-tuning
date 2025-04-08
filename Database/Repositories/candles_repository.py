from sqlalchemy import select
import logging
from Database.database import Database
from Database.TableModel.candle_table import candles_table

class candles_repository():
    def __init__(self):
        self.db = Database()
        
    async def get_oldest_candle_for_interval(self, interval):
        async with self.db.get_session() as session:
            try:
                query = select(candles_table).filter(
                    candles_table.Interval == interval
                ).order_by(candles_table.CloseTime.asc()).limit(1)

                result = await session.execute(query)
                candle = result.scalars().first()
                return candle
            except Exception as e:
                logging.error(f"Error fetching oldest candle: {e}")
                return None

    async def get_candles_by_symbol_timestamp(self, interval, start_timestamp, items_num):
        async with self.db.get_session() as session:
            try:
                query = select(candles_table).filter(
                    candles_table.Interval == interval,
                    candles_table.CloseTime >= start_timestamp
                ).order_by(candles_table.CloseTime.asc()).limit(items_num)
                
                if interval == "30m":
                    a =1

                result = await session.execute(query)
                candles = result.scalars().all()
                return candles
            except Exception as e:
                logging.error(f"Error fetching candles: {e}")
                return None

