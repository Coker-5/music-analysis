import sys

from DrissionPage import Chromium

import pipeline
import scheduler
from spider import DataFetcher


def run_daily_once():
    browser = None
    try:
        browser = Chromium()
        tab = browser.latest_tab
        fetcher = DataFetcher(tab)
        fetcher.get_latest_rank()
    finally:
        if browser is not None:
            browser.quit()
    pipeline.run_daily_pipeline()


def main():
    if len(sys.argv) < 2:
        print("用法: python main.py [history|daily|schedule]")
        raise SystemExit(1)

    mode = sys.argv[1].strip().lower()
    if mode == "history":
        pipeline.run_history_pipeline()
    elif mode == "daily":
        run_daily_once()
    elif mode == "schedule":
        scheduler.start()
    else:
        print("用法: python main.py [history|daily|schedule]")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
