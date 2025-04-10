from Database.TableModel.technical_indicators_table import technical_indicators_table
from Database.database import Database
from sqlalchemy import select
import logging

class technical_indicators_repository:
    def __init__(self):
        self.db = Database()

    async def get_tech_indicators_by_interval(self, interval):
        async with self.db.get_session() as session:
            try:
                query = select(technical_indicators_table).filter(
                    technical_indicators_table.Interval == interval
                ).order_by(technical_indicators_table.CloseTime.asc())
                result = await session.execute(query)
                indicators = result.scalars().all()
                return indicators
            except Exception as e:
                logging.error(f"Error fetching technical indicators: {e}")
                return None