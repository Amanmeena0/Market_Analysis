import logging
import os

log_dir = 'E:\\GenAI\\Market_Analysis\\Market_Researcher\\logs'
os.makedirs(log_dir, exist_ok=True)

# Configure logging to file only (disable console output)
logging.basicConfig(
    level=logging.INFO,
    filename=os.path.join(log_dir, 'logfile.log'),
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    force=True  # Override any existing configuration
)

# Disable console output for all loggers
logging.getLogger().handlers = [h for h in logging.getLogger().handlers if not isinstance(h, logging.StreamHandler)]

# Create a file-only logger
logger = logging.getLogger("MCP_SERVER")
logger.setLevel(logging.INFO)

# Ensure no console handler is added
logger.propagate = False

# Add only file handler if not already present
if not logger.handlers:
    file_handler = logging.FileHandler(os.path.join(log_dir, 'logfile.log'), mode='a')
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
