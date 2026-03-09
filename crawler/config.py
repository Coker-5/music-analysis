import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATICS_DIR = os.path.join(BASE_DIR, "statics")

RESULT_DATA_PATH = os.path.join(STATICS_DIR, "result_data.json")
YEARS_ISSUE_DATA_PATH = os.path.join(STATICS_DIR, "years_issue_data.json")
LATEST_DATA_PATH = os.path.join(STATICS_DIR, "latest_data.json")

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "123456",
    "database": "music_chart",
    "charset": "utf8mb4",
    "autocommit": False,
}

DAILY_CRAWL_HOUR = 8
DAILY_CRAWL_MINUTE = 0
