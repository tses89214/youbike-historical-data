"""
This module define the format of logs, and how we preserve it.
"""
import logging
from logging.handlers import RotatingFileHandler
import os

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(filename)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_DIR = "./logs/"
MAX_LOG_SIZE_BYTES = 1048576  # 1 MB
BACKUP_COUNT = 5  # 保留最近的5個日誌文件

# 檢查日誌目錄是否存在，如不存在則創建
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# 設定 logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# 創建 RotatingFileHandler，設置日誌輸出格式和輪轉條件
file_handler = RotatingFileHandler(
    filename=os.path.join(LOG_DIR, 'log.txt'),
    maxBytes=MAX_LOG_SIZE_BYTES,
    backupCount=BACKUP_COUNT
)
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
file_handler.setFormatter(formatter)

# 添加日誌處理程序到 logger
logger.addHandler(file_handler)
