from Database.database import Database
from Database.TableModel.candle_table import candles_table
import logging

async def initialize_database():
    db = Database()
    async with db.engine.begin() as conn:
        await conn.run_sync(candles_table.metadata.create_all)
    logging.info("Database initialized successfully.")
