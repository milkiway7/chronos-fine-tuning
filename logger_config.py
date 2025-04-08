import logging
def configure_logging():
    logging.basicConfig(
        level=logging.INFO,  # Poziom logowania (INFO, DEBUG, ERROR)
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),  # Wypisuje logi do konsoli
        ]
    )
