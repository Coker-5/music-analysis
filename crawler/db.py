from __future__ import annotations

import json
from datetime import date
from typing import List, Optional

import pymysql

from config import DB_CONFIG
from models import DailyChart, Singer, WeekIssue, WeeklyChart


def get_connection() -> pymysql.Connection:
    return pymysql.connect(
        **DB_CONFIG,
        cursorclass=pymysql.cursors.DictCursor,
    )


def close_connection(conn: Optional[pymysql.Connection]):
    if conn is not None:
        conn.close()


def upsert_singers(conn, singers: List[Singer]):
    if not singers:
        return
    sql = """
        INSERT INTO dim_singer (singer_id, singer_name)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE singer_name = VALUES(singer_name)
    """
    data = [(s.singer_id, s.singer_name) for s in singers]
    with conn.cursor() as cursor:
        cursor.executemany(sql, data)
    conn.commit()


def upsert_week_issues(conn, issues: List[WeekIssue]):
    if not issues:
        return
    sql = """
        INSERT INTO dim_week_issue (issue, year, month, start_date, end_date, title, publish_time)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            title = VALUES(title),
            publish_time = VALUES(publish_time)
    """
    data = [
        (
            issue.issue,
            issue.year,
            issue.month,
            issue.start_date,
            issue.end_date,
            issue.title,
            issue.publish_time,
        )
        for issue in issues
    ]
    with conn.cursor() as cursor:
        cursor.executemany(sql, data)
    conn.commit()


def insert_weekly_charts(conn, charts: List[WeeklyChart]):
    if not charts:
        return

    chart_sql = """
        INSERT INTO fact_weekly_chart (
            issue, year, rank, last_week_rank, song_id, song_name, singer_id, singer_name,
            uni_index, on_chart_weeks, highest_rank, history_highest, new_flag, cover_image
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    exists_sql = """
        SELECT id FROM fact_weekly_chart
        WHERE issue = %s AND rank = %s AND song_id = %s
        LIMIT 1
    """
    index_sql = """
        INSERT INTO fact_weekly_classify_index (
            weekly_id, issue, song_id, index_code, index_name, index_value, percentage, is_champion
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    index_exists_sql = """
        SELECT id FROM fact_weekly_classify_index
        WHERE weekly_id = %s AND index_code = %s
        LIMIT 1
    """

    with conn.cursor() as cursor:
        for idx, chart in enumerate(charts, start=1):
            cursor.execute(exists_sql, (chart.issue, chart.rank, chart.song_id))
            existing = cursor.fetchone()
            weekly_id = existing["id"] if existing else None

            if weekly_id is None:
                cursor.execute(
                    chart_sql,
                    (
                        chart.issue,
                        chart.year,
                        chart.rank,
                        chart.last_week_rank,
                        chart.song_id,
                        chart.song_name,
                        chart.singer_id,
                        chart.singer_name,
                        chart.uni_index,
                        chart.on_chart_weeks,
                        chart.highest_rank,
                        chart.history_highest,
                        chart.new_flag,
                        chart.cover_image,
                    ),
                )
                weekly_id = cursor.lastrowid

            if weekly_id and chart.indices:
                for index in chart.indices:
                    cursor.execute(index_exists_sql, (weekly_id, index.index_code))
                    if cursor.fetchone():
                        continue
                    index.weekly_id = weekly_id
                    cursor.execute(
                        index_sql,
                        (
                            index.weekly_id,
                            index.issue,
                            index.song_id,
                            index.index_code,
                            index.index_name,
                            index.index_value,
                            index.percentage,
                            index.is_champion,
                        ),
                    )

            if idx % 500 == 0:
                conn.commit()

    conn.commit()


def is_weekly_data_exists(conn) -> bool:
    sql = "SELECT COUNT(*) AS count FROM fact_weekly_chart"
    with conn.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchone()
    return bool(result and result["count"] > 0)


def upsert_daily_charts(conn, charts: List[DailyChart]):
    if not charts:
        return
    sql = """
        INSERT INTO fact_daily_chart (
            chart_date, issue, rank, pre_rank, incr_rank, song_id, song_name, singer_id, singer_name,
            score, pre_score, incr_score, play_index, pay_index, pop_index, days_on_chart, high_rank,
            high_index, new_flag, first_on_chart, track_tags, cover_image, publish_time
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            score = VALUES(score),
            incr_rank = VALUES(incr_rank),
            incr_score = VALUES(incr_score),
            play_index = VALUES(play_index),
            pay_index = VALUES(pay_index),
            pop_index = VALUES(pop_index),
            track_tags = VALUES(track_tags)
    """
    data = [
        (
            chart.chart_date,
            chart.issue,
            chart.rank,
            chart.pre_rank,
            chart.incr_rank,
            chart.song_id,
            chart.song_name,
            chart.singer_id,
            chart.singer_name,
            chart.score,
            chart.pre_score,
            chart.incr_score,
            chart.play_index,
            chart.pay_index,
            chart.pop_index,
            chart.days_on_chart,
            chart.high_rank,
            chart.high_index,
            chart.new_flag,
            chart.first_on_chart,
            json.dumps(chart.track_tags, ensure_ascii=False) if chart.track_tags is not None else None,
            chart.cover_image,
            chart.publish_time,
        )
        for chart in charts
    ]
    with conn.cursor() as cursor:
        cursor.executemany(sql, data)
    conn.commit()


def get_latest_daily_date(conn) -> date | None:
    sql = "SELECT MAX(chart_date) AS latest_date FROM fact_daily_chart"
    with conn.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchone()
    return result["latest_date"] if result else None


def refresh_agg_singer_yearly(conn):
    sql = """
        INSERT INTO agg_singer_yearly
            (singer_id, singer_name, year, chart_count, top3_count, champion_count, avg_rank, avg_index)
        SELECT
            singer_id,
            singer_name,
            year,
            COUNT(*) AS chart_count,
            SUM(CASE WHEN rank <= 3 THEN 1 ELSE 0 END) AS top3_count,
            SUM(CASE WHEN rank = 1 THEN 1 ELSE 0 END) AS champion_count,
            ROUND(AVG(rank), 2) AS avg_rank,
            ROUND(AVG(uni_index), 2) AS avg_index
        FROM fact_weekly_chart
        GROUP BY singer_id, singer_name, year
        ON DUPLICATE KEY UPDATE
            chart_count = VALUES(chart_count),
            top3_count = VALUES(top3_count),
            champion_count = VALUES(champion_count),
            avg_rank = VALUES(avg_rank),
            avg_index = VALUES(avg_index)
    """
    with conn.cursor() as cursor:
        cursor.execute(sql)
    conn.commit()


def refresh_agg_song_longevity(conn):
    sql = """
        INSERT INTO agg_song_longevity
            (song_id, song_name, singer_id, singer_name, total_weeks, history_best_rank,
             first_chart_date, last_chart_date, champion_weeks, cover_image)
        SELECT
            f.song_id,
            f.song_name,
            f.singer_id,
            f.singer_name,
            COUNT(*) AS total_weeks,
            MIN(f.rank) AS history_best_rank,
            MIN(i.start_date) AS first_chart_date,
            MAX(i.end_date) AS last_chart_date,
            SUM(CASE WHEN f.rank = 1 THEN 1 ELSE 0 END) AS champion_weeks,
            MAX(f.cover_image) AS cover_image
        FROM fact_weekly_chart f
        LEFT JOIN dim_week_issue i ON f.issue = i.issue
        GROUP BY f.song_id, f.song_name, f.singer_id, f.singer_name
        ON DUPLICATE KEY UPDATE
            total_weeks = VALUES(total_weeks),
            history_best_rank = VALUES(history_best_rank),
            first_chart_date = VALUES(first_chart_date),
            last_chart_date = VALUES(last_chart_date),
            champion_weeks = VALUES(champion_weeks),
            cover_image = VALUES(cover_image)
    """
    with conn.cursor() as cursor:
        cursor.execute(sql)
    conn.commit()


def refresh_agg_singer_total(conn):
    sql = """
        INSERT INTO agg_singer_total
            (singer_id, singer_name, total_count, champion_count, top3_count,
             distinct_songs, best_rank, active_years, first_chart_year, last_chart_year)
        SELECT
            singer_id,
            singer_name,
            COUNT(*) AS total_count,
            SUM(CASE WHEN rank = 1 THEN 1 ELSE 0 END) AS champion_count,
            SUM(CASE WHEN rank <= 3 THEN 1 ELSE 0 END) AS top3_count,
            COUNT(DISTINCT song_id) AS distinct_songs,
            MIN(rank) AS best_rank,
            COUNT(DISTINCT year) AS active_years,
            MIN(year) AS first_chart_year,
            MAX(year) AS last_chart_year
        FROM fact_weekly_chart
        GROUP BY singer_id, singer_name
        ON DUPLICATE KEY UPDATE
            total_count = VALUES(total_count),
            champion_count = VALUES(champion_count),
            top3_count = VALUES(top3_count),
            distinct_songs = VALUES(distinct_songs),
            best_rank = VALUES(best_rank),
            active_years = VALUES(active_years),
            first_chart_year = VALUES(first_chart_year),
            last_chart_year = VALUES(last_chart_year)
    """
    with conn.cursor() as cursor:
        cursor.execute(sql)
    conn.commit()


def refresh_all_agg(conn):
    refresh_agg_singer_yearly(conn)
    print("agg_singer_yearly 刷新完成")
    refresh_agg_song_longevity(conn)
    print("agg_song_longevity 刷新完成")
    refresh_agg_singer_total(conn)
    print("agg_singer_total 刷新完成")

