from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from DrissionPage import Chromium

import pipeline
from config import DAILY_CRAWL_HOUR, DAILY_CRAWL_MINUTE
from spider import DataFetcher


def daily_job():
    browser = None
    try:
        print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] 开始执行日榜定时任务")
        browser = Chromium()
        tab = browser.latest_tab
        fetcher = DataFetcher(tab)
        fetcher.get_latest_rank()
        pipeline.run_daily_pipeline()
        print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] 日榜定时任务完成")
    except Exception as exc:
        print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] 日榜定时任务失败: {exc}")
    finally:
        if browser is not None:
            browser.quit()


def start():
    scheduler = BlockingScheduler()
    scheduler.add_job(
        daily_job,
        "cron",
        hour=DAILY_CRAWL_HOUR,
        minute=DAILY_CRAWL_MINUTE,
    )
    print(f"定时调度已启动，每天 {DAILY_CRAWL_HOUR:02d}:{DAILY_CRAWL_MINUTE:02d} 执行")
    scheduler.start()
