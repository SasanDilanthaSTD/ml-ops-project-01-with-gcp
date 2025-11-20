# import nessary dependancies
import logging
import os
from datetime import datetime

# define logger directory and file
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, f'log__{datetime.now().strftime("%d-%m-%y")}.log ')

# configure logger 
logging.basicConfig(
    filename=LOG_FILE,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def get_logger(name):
    """Function to get the logger instance."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger