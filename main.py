import asyncio
from Database.database_init import initialize_database
from logger_config import configure_logging
from Modules.prepare_data_for_fine_tuning import DataProcessor
configure_logging()

async def main():
    await initialize_database()
    processor = DataProcessor()
    await processor.process_data()

if __name__ == "__main__":
    asyncio.run(main())