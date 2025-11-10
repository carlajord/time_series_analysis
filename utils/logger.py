import os
import logging
import datetime


LOG_FILE_PATH = os.path.join(os.path.dirname(__file__), "..", "logs")

def init_log():
    
    os.makedirs(LOG_FILE_PATH, exist_ok=True)
    filename = os.path.join(LOG_FILE_PATH, "pipeline.log")
    with open(filename, 'w') as f:
        f.write(f"Log file created at {datetime.datetime.now()}\n")
    print("Log file created:", filename)
    

def setup_logging():

    init_log()
    
    logging.basicConfig(
        filename=os.path.join(LOG_FILE_PATH, "pipeline.log"),
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )
    logging.getLogger().addHandler(console_handler)
