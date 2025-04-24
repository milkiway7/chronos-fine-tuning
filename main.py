import asyncio
from Database.database_init import initialize_database
from logger_config import configure_logging
from Modules.prepare_candle_data_for_fine_tuning import candle_data_processor
from Modules.prepare_tech_indicators_data_fine_tuning import tech_indicators_data_processor
from Database.Repositories.candles_repository import candles_repository
from Modules.scaler import Scaler
configure_logging()

async def main():
    await initialize_database()
    candles_repository_instance = candles_repository()
    processor = candle_data_processor(candles_repository_instance)
    async for df in processor.process_data():
        scaler = Scaler(df)
        scaler.scale()
        a = df

        # add tokens to 
    # technical_processor = tech_indicators_data_processor()
    # await technical_processor.process_data()
if __name__ == "__main__":
    asyncio.run(main())