# app/logger.py

import logging

logger = logging.getLogger("rag-logger")
logger.setLevel(logging.DEBUG)

# Stampa tutto su console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter("[%(levelname)s] %(message)s")
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)
