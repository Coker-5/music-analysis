# datashow/db_query.py

from django.db import connection


def dictfetchall(cursor):
    """将 cursor 查询结果转为字典列表"""
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def dictfetchone(cursor):
    """将 cursor 单行结果转为字典"""
    columns = [col[0] for col in cursor.description]
    row = cursor.fetchone()
    return dict(zip(columns, row)) if row else {}


# ================================================================
# head 接口：顶部今日核心指标数字卡片
# 对应大屏：③ 中上数字卡片区（5个指标）
# 查询表：fact_daily_chart（取最新日期数据）
#
# 返回格式：
# {
#   "chart_date": "2026-03-09",
#   "champion_song": "吉量",
#   "champion_singer": "周深",
#   "champion_cover": "https://...",
#   "avg_score": 77.35,
#   "top10_new_count": 2,
#   "max_incr_song": "某歌曲",
#   "max_incr_value": 5
# }
# ================================================================
def query_head():
    with connection.cursor() as cursor:
        # 1. 获取最新榜单日期
        cursor.execute("SELECT MAX(chart_date) AS latest FROM fact_daily_chart")
        latest_date = dictfetchone(cursor)['latest']

        if not latest_date:
            return {}

        # 2. 今日冠军（rank=1）
        cursor.execute("""
            SELECT song_name, singer_name, cover_image
            FROM fact_daily_chart
            WHERE chart_date = %s AND `rank` = 1
            LIMIT 1
        """, [latest_date])
        champion = dictfetchone(cursor)

        # 3. 今日平均得分
        cursor.execute("""
            SELECT ROUND(AVG(score), 2) AS avg_score
            FROM fact_daily_chart
            WHERE chart_date = %s
        """, [latest_date])
        avg = dictfetchone(cursor)

        # 4. 今日 TOP10 中新入榜数量（new_flag=1 且 rank<=10）
        cursor.execute("""
            SELECT COUNT(*) AS cnt
            FROM fact_daily_chart
            WHERE chart_date = %s AND `rank` <= 10 AND new_flag = 1
        """, [latest_date])
        new_count = dictfetchone(cursor)

        # 5. 今日涨幅最大的歌曲（incr_rank 最大正值）
        cursor.execute("""
            SELECT song_name, incr_rank
            FROM fact_daily_chart
            WHERE chart_date = %s AND incr_rank > 0
            ORDER BY incr_rank DESC
            LIMIT 1
        """, [latest_date])
        max_incr = dictfetchone(cursor)

    return {
        "chart_date":      str(latest_date),
        "champion_song":   champion.get("song_name", ""),
        "champion_singer": champion.get("singer_name", ""),
        "champion_cover":  champion.get("cover_image", ""),
        "avg_score":       float(avg.get("avg_score") or 0),
        "top10_new_count": int(new_count.get("cnt") or 0),
        "max_incr_song":   max_incr.get("song_name", ""),
        "max_incr_value":  int(max_incr.get("incr_rank") or 0),
    }


# ================================================================
# centerLeft1 接口：歌手上榜占比饼图
# 对应大屏：① 左上一饼图
# 查询表：agg_singer_total（取 total_count 前10）
#
# 返回格式：
# [
#   {"singer_name": "周深", "total_count": 156},
#   {"singer_name": "薛之谦", "total_count": 98},
#   ...（共10条）
# ]
# ================================================================
def query_center_left1():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT singer_name, total_count
            FROM agg_singer_total
            ORDER BY total_count DESC
            LIMIT 10
        """)
        return dictfetchall(cursor)


# ================================================================
# centerLeft2 接口：歌手词云图
# 对应大屏：② 左上二词云
# 查询表：agg_singer_total（取 total_count 前50，词云需要更多数据量）
#
# 返回格式：
# [
#   {"name": "周深", "value": 156},
#   {"name": "薛之谦", "value": 98},
#   ...（共50条）
# ]
# ================================================================
def query_center_left2():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT singer_name AS name, total_count AS value
            FROM agg_singer_total
            ORDER BY total_count DESC
            LIMIT 50
        """)
        return dictfetchall(cursor)


# ================================================================
# centerData 接口：中上横向 Top 歌手条形图
# 对应大屏：④ 中右上横向条形图
# 查询表：agg_singer_total（取前10）
#
# 返回格式：
# {
#   "singers": ["周深", "薛之谦", "邓紫棋", ...],
#   "counts":  [156, 98, 87, ...]
# }
# ================================================================
def query_center_data():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT singer_name, total_count, champion_count, top3_count
            FROM agg_singer_total
            ORDER BY total_count DESC
            LIMIT 10
        """)
        rows = dictfetchall(cursor)

    return {
        "singers":        [r["singer_name"]   for r in rows],
        "counts":         [r["total_count"]   for r in rows],
        "champion_counts":[r["champion_count"] for r in rows],
        "top3_counts":    [r["top3_count"]    for r in rows],
    }


# ================================================================
# centerRight1 接口：今日 Top1 三维指数环形仪表盘
# 对应大屏：⑤ 中右三个环形图
# 查询表：fact_daily_chart（最新日期 rank=1）
#
# 返回格式：
# {
#   "song_name":  "吉量",
#   "singer_name": "周深",
#   "play_index":  75.35,
#   "pay_index":   84.94,
#   "pop_index":   90.22
# }
# ================================================================
def query_center_right1():
    with connection.cursor() as cursor:
        cursor.execute("SELECT MAX(chart_date) AS latest FROM fact_daily_chart")
        latest_date = dictfetchone(cursor)['latest']
        if not latest_date:
            return {}

        cursor.execute("""
            SELECT song_name, singer_name, play_index, pay_index, pop_index
            FROM fact_daily_chart
            WHERE chart_date = %s AND `rank` = 1
            LIMIT 1
        """, [latest_date])
        row = dictfetchone(cursor)

    return {
        "song_name":   row.get("song_name", ""),
        "singer_name": row.get("singer_name", ""),
        "play_index":  float(row.get("play_index") or 0),
        "pay_index":   float(row.get("pay_index") or 0),
        "pop_index":   float(row.get("pop_index") or 0),
    }


# ================================================================
# centerRight2 接口：今日得分区间分布 + 长红歌曲留榜排行
# 对应大屏：⑥ 得分区间分布图 + ⑦ 长红歌曲留榜表
# 查询表：fact_daily_chart（区间分布）+ agg_song_longevity（留榜排行）
#
# 返回格式：
# {
#   "score_distribution": [
#     {"range": "90-100", "count": 12},
#     {"range": "80-90",  "count": 45},
#     {"range": "70-80",  "count": 89},
#     {"range": "60-70",  "count": 54}
#   ],
#   "longevity_top8": [
#     {
#       "song_name": "歌曲名",
#       "singer_name": "歌手名",
#       "total_weeks": 88,
#       "history_best_rank": 1,
#       "champion_weeks": 12,
#       "cover_image": "https://..."
#     },
#     ...（共8条）
#   ]
# }
# ================================================================
def query_center_right2():
    with connection.cursor() as cursor:
        # 1. 今日得分区间分布
        cursor.execute("SELECT MAX(chart_date) AS latest FROM fact_daily_chart")
        latest_date = dictfetchone(cursor)['latest']

        cursor.execute("""
            SELECT
                CASE
                    WHEN score >= 90 THEN '90-100'
                    WHEN score >= 80 THEN '80-90'
                    WHEN score >= 70 THEN '70-80'
                    ELSE '60-70'
                END AS `range`,
                COUNT(*) AS count
            FROM fact_daily_chart
            WHERE chart_date = %s
            GROUP BY `range`
            ORDER BY `range` DESC
        """, [latest_date])
        distribution = dictfetchall(cursor)

        # 2. 长红歌曲 Top8
        cursor.execute("""
            SELECT song_name, singer_name, total_weeks,
                   history_best_rank, champion_weeks, cover_image
            FROM agg_song_longevity
            ORDER BY total_weeks DESC
            LIMIT 8
        """)
        longevity = dictfetchall(cursor)

    return {
        "score_distribution": distribution,
        "longevity_top8":     longevity,
    }


# ================================================================
# bottomLeft 接口：今日实时榜单滚动表
# 对应大屏：⑧ 左下 Top200 滚动表
# 查询表：fact_daily_chart（最新日期，全部200条，按 rank 排序）
#
# 返回格式：
# [
#   {
#     "rank": 1,
#     "song_name": "吉量",
#     "singer_name": "周深",
#     "score": 96.98,
#     "incr_rank": 0,
#     "incr_score": 0.03,
#     "days_on_chart": 19,
#     "track_tags": ["夺冠14天", "五连冠"],
#     "cover_image": "https://..."
#   },
#   ...（最多200条）
# ]
# ================================================================
def query_bottom_left():
    import json as _json
    with connection.cursor() as cursor:
        cursor.execute("SELECT MAX(chart_date) AS latest FROM fact_daily_chart")
        latest_date = dictfetchone(cursor)['latest']
        if not latest_date:
            return []

        cursor.execute("""
            SELECT `rank`, song_name, singer_name, score,
                   incr_rank, incr_score, days_on_chart,
                   track_tags, cover_image
            FROM fact_daily_chart
            WHERE chart_date = %s
            ORDER BY `rank` ASC
        """, [latest_date])
        rows = dictfetchall(cursor)

    # track_tags 存的是 JSON 字符串，需要反序列化
    for row in rows:
        if row.get("track_tags") and isinstance(row["track_tags"], str):
            try:
                row["track_tags"] = _json.loads(row["track_tags"])
            except Exception:
                row["track_tags"] = []
        # 数值字段转 float/int 确保可序列化
        row["score"]       = float(row["score"] or 0)
        row["incr_score"]  = float(row["incr_score"] or 0)
        row["incr_rank"]   = int(row["incr_rank"] or 0)
        row["days_on_chart"] = int(row["days_on_chart"] or 0)

    return rows


# ================================================================
# bottomRight 接口：歌手历年演化 3D 柱状图
# 对应大屏：⑨ 右下历年演化 3D 柱状图
# 查询表：agg_singer_yearly
# 取：total_count 全期合计前8的歌手，展示其 2018-2025 各年上榜次数
#
# 返回格式：
# {
#   "years": [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
#   "singers": ["周深", "薛之谦", "邓紫棋", ...],   ← 共8个
#   "series": [
#     {
#       "singer": "周深",
#       "data": [3, 8, 12, 20, 25, 30, 35, 23]   ← 与 years 对应，无数据补0
#     },
#     ...
#   ]
# }
# ================================================================
def query_bottom_right():
    with connection.cursor() as cursor:
        # 1. 取上榜总次数前8的歌手
        cursor.execute("""
            SELECT singer_id, singer_name
            FROM agg_singer_total
            ORDER BY total_count DESC
            LIMIT 8
        """)
        top_singers = dictfetchall(cursor)

        if not top_singers:
            return {"years": [], "singers": [], "series": []}

        singer_ids = [s["singer_id"] for s in top_singers]
        singer_names = [s["singer_name"] for s in top_singers]

        # 2. 查这8个歌手在所有年份的上榜次数
        placeholders = ",".join(["%s"] * len(singer_ids))
        cursor.execute(f"""
            SELECT singer_id, year, chart_count
            FROM agg_singer_yearly
            WHERE singer_id IN ({placeholders})
            ORDER BY year ASC
        """, singer_ids)
        yearly_rows = dictfetchall(cursor)

        # 3. 获取所有年份列表
        cursor.execute("""
            SELECT DISTINCT year FROM agg_singer_yearly ORDER BY year ASC
        """)
        years = [r["year"] for r in dictfetchall(cursor)]

    # 4. 构建二维映射 {singer_id: {year: chart_count}}
    data_map = {sid: {} for sid in singer_ids}
    for row in yearly_rows:
        sid = row["singer_id"]
        if sid in data_map:
            data_map[sid][row["year"]] = row["chart_count"]

    # 5. 组装 series，无数据的年份补0
    series = []
    for singer in top_singers:
        sid = singer["singer_id"]
        series.append({
            "singer": singer["singer_name"],
            "data":   [int(data_map[sid].get(y, 0)) for y in years],
        })

    return {
        "years":   years,
        "singers": singer_names,
        "series":  series,
    }
