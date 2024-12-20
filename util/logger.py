import logging
import os
from datetime import datetime, timedelta

# Configure the log directory and file names
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Determine the log file name for today
LOG_FILE = os.path.join(LOG_DIR, f"app_log_{datetime.now().strftime('%Y%m%d')}.log")

# Remove today's log file if it already exists
if os.path.exists(LOG_FILE):
    try:
        os.remove(LOG_FILE)
        print(f"Today's log file removed: {LOG_FILE}")
    except Exception as e:
        print(f"Failed to remove today's log file: {e}")

# Determine the log file name for yesterday (to remove old logs)
OLD_LOG_FILE = os.path.join(LOG_DIR, f"app_log_{(datetime.now() - timedelta(days=1)).strftime('%Y%m%d')}.log")

# Remove yesterday's log file if it exists
if os.path.exists(OLD_LOG_FILE):
    try:
        os.remove(OLD_LOG_FILE)
        print(f"Old log file removed: {OLD_LOG_FILE}")
    except Exception as e:
        print(f"Failed to remove old log file: {e}")

# Check if the logger is already configured to avoid reinitialization
if not logging.getLogger("Cionix").hasHandlers():
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] [%(module)s:%(funcName)s] %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE),  # Log to file
            logging.StreamHandler(),        # Optional: Log to console
        ],
    )

# Create a logger instance
logger = logging.getLogger("Cionix")

# Log application start
logger.info("Logger initialized.")
