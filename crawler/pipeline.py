from __future__ import annotations

from datetime import date, datetime

import cleaner
import db
from config import LATEST_DATA_PATH, RESULT_DATA_PATH, YEARS_ISSUE_DATA_PATH


def _log_step(message: str, start_time: datetime):
    cost = (datetime.now() - start_time).total_seconds()
    print(f"{message}，耗时 {cost:.2f}s")


def run_history_pipeline():
    conn = None
    total_start = datetime.now()
    try:
        print("开始执行历史数据全量导入...")
        conn = db.get_connection()

        step_start = datetime.now()
        if db.is_weekly_data_exists(conn):
            _log_step("检测到 fact_weekly_chart 已有数据，跳过历史导入", step_start)
            return
        _log_step("历史数据空表检查完成", step_start)

        step_start = datetime.now()
        issues = cleaner.load_and_parse_years_issue(YEARS_ISSUE_DATA_PATH)
        _log_step(f"期数元数据解析完成，共 {len(issues)} 条", step_start)

        step_start = datetime.now()
        db.upsert_week_issues(conn, issues)
        _log_step("期数元数据入库完成", step_start)

        step_start = datetime.now()
        singers, charts = cleaner.load_and_parse_weekly(RESULT_DATA_PATH)
        _log_step(f"历史周榜解析完成，歌手 {len(singers)} 条，周榜 {len(charts)} 条", step_start)

        step_start = datetime.now()
        db.upsert_singers(conn, singers)
        _log_step("歌手维度写入完成", step_start)

        step_start = datetime.now()
        db.insert_weekly_charts(conn, charts)
        _log_step("历史周榜与分类指标写入完成", step_start)

        step_start = datetime.now()
        db.refresh_all_agg(conn)
        _log_step("聚合表刷新完成", step_start)

        _log_step("历史数据全量导入完成", total_start)
    finally:
        db.close_connection(conn)


def run_daily_pipeline():
    conn = None
    today = date.today()
    try:
        print(f"开始执行日榜入库，日期: {today}")
        conn = db.get_connection()
        singers, charts = cleaner.load_and_parse_daily(LATEST_DATA_PATH, today)
        db.upsert_singers(conn, singers)
        db.upsert_daily_charts(conn, charts)
        print(f"日榜入库完成，日期: {today}，歌手 {len(singers)} 条，榜单 {len(charts)} 条")
    finally:
        db.close_connection(conn)

