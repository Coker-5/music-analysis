# datashow/views.py

import json
from decimal import Decimal
from datetime import date, datetime
from django.http import JsonResponse
from datashow import db_query


class MusicJSONEncoder(json.JSONEncoder):
    """
    自定义 JSON 序列化器，处理 MySQL 返回的特殊类型：
    - Decimal  → float
    - date     → "YYYY-MM-DD" 字符串
    - datetime → "YYYY-MM-DD HH:MM:SS" 字符串
    """
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        return super().default(obj)


def api_response(data):
    """统一返回函数，使用自定义 encoder，设置跨域头"""
    content = json.dumps(data, cls=MusicJSONEncoder, ensure_ascii=False)
    return JsonResponse(
        json.loads(content),
        safe=False,
        json_dumps_params={"ensure_ascii": False}
    )


def head(request):
    """顶部今日核心指标数字卡片"""
    try:
        data = db_query.query_head()
    except Exception as e:
        data = {"error": str(e)}
    return api_response(data)


def centerLeft1(request):
    """歌手上榜占比饼图"""
    try:
        data = db_query.query_center_left1()
    except Exception as e:
        data = {"error": str(e)}
    return api_response(data)


def centerLeft2(request):
    """歌手词云图"""
    try:
        data = db_query.query_center_left2()
    except Exception as e:
        data = {"error": str(e)}
    return api_response(data)


def center_data(request):
    """Top 歌手上榜次数横向条形图"""
    try:
        data = db_query.query_center_data()
    except Exception as e:
        data = {"error": str(e)}
    return api_response(data)


def centerRight1(request):
    """今日 Top1 三维指数环形仪表盘"""
    try:
        data = db_query.query_center_right1()
    except Exception as e:
        data = {"error": str(e)}
    return api_response(data)


def centerRight2(request):
    """今日得分区间分布 + 长红歌曲留榜排行"""
    try:
        data = db_query.query_center_right2()
    except Exception as e:
        data = {"error": str(e)}
    return api_response(data)


def bottomLeft(request):
    """今日实时榜单滚动表（Top200）"""
    try:
        data = db_query.query_bottom_left()
    except Exception as e:
        data = {"error": str(e)}
    return api_response(data)


def bottomRight(request):
    """歌手历年演化 3D 柱状图"""
    try:
        data = db_query.query_bottom_right()
    except Exception as e:
        data = {"error": str(e)}
    return api_response(data)
