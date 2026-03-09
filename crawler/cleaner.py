from __future__ import annotations

import json
from datetime import date, datetime
from typing import Any, Dict, List, Optional

from models import DailyChart, Singer, WeekIssue, WeeklyChart, WeeklyClassifyIndex


def to_float(val) -> Optional[float]:
    if val is None or val == "":
        return None
    try:
        return float(val)
    except (TypeError, ValueError):
        return None


def to_int(val) -> Optional[int]:
    if val is None or val == "":
        return None
    try:
        return int(val)
    except (TypeError, ValueError):
        return None


def to_bool_int(val) -> int:
    if isinstance(val, bool):
        return int(val)
    if isinstance(val, int):
        return 1 if val != 0 else 0
    if isinstance(val, str):
        return 1 if val.strip().lower() in {"1", "true", "yes", "y"} else 0
    return 0


def parse_datetime(val: Optional[str]) -> Optional[datetime]:
    if not val:
        return None
    try:
        return datetime.strptime(val, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None


def parse_date(val: Optional[str]) -> Optional[date]:
    dt = parse_datetime(val)
    return dt.date() if dt else None


def parse_years_issue(data: Dict) -> List[WeekIssue]:
    issues: List[WeekIssue] = []
    for issue_items in data.values():
        if not isinstance(issue_items, list):
            continue
        for item in issue_items:
            issue = str(item.get("issue", "")).strip()
            start_date = parse_date(item.get("startTime"))
            end_date = parse_date(item.get("endTime"))
            month = to_int(item.get("month"))
            if not issue or start_date is None or end_date is None or month is None:
                continue
            issues.append(
                WeekIssue(
                    issue=issue,
                    year=int(issue[:4]),
                    month=month,
                    start_date=start_date,
                    end_date=end_date,
                    title=item.get("title"),
                    publish_time=parse_datetime(item.get("publishTime")),
                )
            )
    return issues


def parse_weekly_chart(data: Dict) -> tuple[List[Singer], List[WeeklyChart]]:
    singers_map: Dict[str, Singer] = {}
    charts: List[WeeklyChart] = []

    for year_key, year_issues in data.items():
        year = to_int(year_key)
        if year is None or not isinstance(year_issues, dict):
            continue
        for issue, song_list in year_issues.items():
            if not isinstance(song_list, list):
                continue
            for item in song_list:
                singer_id = str(item.get("singerId", "")).strip()
                singer_name = str(item.get("singerName", "")).strip()
                song_id = str(item.get("songId", "")).strip()
                song_name = str(item.get("songName", "")).strip()
                rank = to_int(item.get("rank"))
                if not singer_id or not singer_name or not song_id or not song_name or rank is None:
                    continue

                singers_map.setdefault(
                    singer_id,
                    Singer(singer_id=singer_id, singer_name=singer_name),
                )

                indices: List[WeeklyClassifyIndex] = []
                for index_item in item.get("classifyIndices") or []:
                    index_code = to_int(index_item.get("code"))
                    index_name = str(index_item.get("name", "")).strip()
                    if index_code is None or not index_name:
                        continue
                    indices.append(
                        WeeklyClassifyIndex(
                            weekly_id=0,
                            issue=str(issue),
                            song_id=song_id,
                            index_code=index_code,
                            index_name=index_name,
                            index_value=to_float(index_item.get("index")),
                            percentage=to_int(index_item.get("percentage")),
                            is_champion=to_bool_int(index_item.get("isChampion")),
                        )
                    )

                charts.append(
                    WeeklyChart(
                        issue=str(issue),
                        year=year,
                        rank=rank,
                        last_week_rank=to_int(item.get("lastWeekRank")),
                        song_id=song_id,
                        song_name=song_name,
                        singer_id=singer_id,
                        singer_name=singer_name,
                        uni_index=to_float(item.get("uniIndex")),
                        on_chart_weeks=to_int(item.get("onChartWeeks")),
                        highest_rank=to_int(item.get("highestRank")),
                        history_highest=to_int(item.get("historyHighestRank")),
                        new_flag=to_bool_int(item.get("newFlag")),
                        cover_image=item.get("coverImages"),
                        indices=indices,
                    )
                )

    return list(singers_map.values()), charts


def parse_daily_chart(data: List[Dict], chart_date: date) -> tuple[List[Singer], List[DailyChart]]:
    singers_map: Dict[str, Singer] = {}
    charts: List[DailyChart] = []

    for item in data:
        info = item.get("info") or {}
        extend = item.get("extend") or {}

        singer_id = str(info.get("singerId", "")).strip() or None
        singer_name = str(info.get("singerName", "")).strip()
        song_id = str(item.get("itemId", "")).strip()
        song_name = str(info.get("trackNameShow", "")).strip()
        issue = str(item.get("issue", "")).strip()
        rank = to_int(item.get("rank"))
        score = to_float(item.get("score"))

        if singer_id and singer_name:
            singers_map.setdefault(
                singer_id,
                Singer(singer_id=singer_id, singer_name=singer_name),
            )

        if not issue or not song_id or not song_name or not singer_name or rank is None or score is None:
            continue

        track_tags = item.get("trackTags")
        charts.append(
            DailyChart(
                chart_date=chart_date,
                issue=issue,
                rank=rank,
                pre_rank=to_int(item.get("preRank")),
                incr_rank=to_int(item.get("incrRank")),
                song_id=song_id,
                song_name=song_name,
                singer_id=singer_id,
                singer_name=singer_name,
                score=score,
                pre_score=to_float(item.get("preScore")),
                incr_score=to_float(item.get("incrScore")),
                play_index=to_float(extend.get("playIndex")),
                pay_index=to_float(extend.get("payIndex")),
                pop_index=to_float(extend.get("popIndex")),
                days_on_chart=to_int(extend.get("days")),
                high_rank=to_int(extend.get("highRank")),
                high_index=to_float(extend.get("highIndex")),
                new_flag=to_bool_int(extend.get("newFlag")),
                first_on_chart=to_bool_int(item.get("firstOnChart")),
                track_tags=track_tags if isinstance(track_tags, list) else None,
                cover_image=info.get("coverImages"),
                publish_time=parse_datetime(info.get("publishTime")),
            )
        )

    return list(singers_map.values()), charts


def _load_json(filepath: str) -> Any:
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)


def load_and_parse_years_issue(filepath: str) -> List[WeekIssue]:
    return parse_years_issue(_load_json(filepath))


def load_and_parse_weekly(filepath: str) -> tuple[List[Singer], List[WeeklyChart]]:
    return parse_weekly_chart(_load_json(filepath))


def load_and_parse_daily(filepath: str, chart_date: date) -> tuple[List[Singer], List[DailyChart]]:
    return parse_daily_chart(_load_json(filepath), chart_date)

