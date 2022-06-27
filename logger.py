import logging

logging.basicConfig(
    level=logging.INFO,
    filename="log/app.log",
    format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
    datefmt='%d/%m/%Y %H:%M:%S',
    )
