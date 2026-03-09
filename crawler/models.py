from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import List, Optional


@dataclass
class Singer:
    singer_id: str
    singer_name: str


@dataclass
class WeekIssue:
    issue: str
    year: int
    month: int
    start_date: date
    end_date: date
    title: Optional[str] = None
    publish_time: Optional[datetime] = None


@dataclass
class WeeklyClassifyIndex:
    weekly_id: int
    issue: str
    song_id: str
    index_code: int
    index_name: str
    index_value: Optional[float] = None
    percentage: Optional[int] = None
    is_champion: int = 0


@dataclass
class WeeklyChart:
    issue: str
    year: int
    rank: int
    last_week_rank: Optional[int]
    song_id: str
    song_name: str
    singer_id: str
    singer_name: str
    uni_index: Optional[float] = None
    on_chart_weeks: Optional[int] = None
    highest_rank: Optional[int] = None
    history_highest: Optional[int] = None
    new_flag: int = 0
    cover_image: Optional[str] = None
    indices: List[WeeklyClassifyIndex] = field(default_factory=list)


@dataclass
class DailyChart:
    chart_date: date
    issue: str
    rank: int
    pre_rank: Optional[int]
    incr_rank: Optional[int]
    song_id: str
    song_name: str
    singer_id: Optional[str]
    singer_name: str
    score: float
    pre_score: Optional[float]
    incr_score: Optional[float]
    play_index: Optional[float]
    pay_index: Optional[float]
    pop_index: Optional[float]
    days_on_chart: Optional[int]
    high_rank: Optional[int]
    high_index: Optional[float]
    new_flag: int = 0
    first_on_chart: int = 0
    track_tags: Optional[List[str]] = None
    cover_image: Optional[str] = None
    publish_time: Optional[datetime] = None

