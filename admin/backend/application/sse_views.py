# views.py
import time

import jwt
from jwt import InvalidTokenError
from django.http import StreamingHttpResponse, HttpResponse

from application import settings
from dvadmin.system.models import MessageCenterTargetUser
from django.core.cache import cache


def event_stream(user_id):
    last_sent_time = 0

    while True:
        # 从 Redis 中获取最后数据库变更时间
        try:
            last_db_change_time = cache.get('last_db_change_time', 0)
        except Exception:
            # Redis unavailable: fall back to polling
            last_db_change_time = time.time()
        # 只有当数据库发生变化时才检查总数
        if last_db_change_time and last_db_change_time > last_sent_time:
            try:
                count = MessageCenterTargetUser.objects.filter(users=user_id, is_read=False).count()
            except Exception:
                count = 0
            yield f"data: {count}\n\n"
            last_sent_time = time.time()

        time.sleep(1)


def sse_view(request):
    token = request.GET.get('token')
    if not token:
        return HttpResponse(status=401)
    try:
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    except InvalidTokenError:
        return HttpResponse(status=401)
    user_id = decoded.get('user_id')
    response = StreamingHttpResponse(event_stream(user_id), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    # Explicit CORS headers for EventSource
    origin = request.headers.get('Origin')
    if origin:
        response['Access-Control-Allow-Origin'] = origin
        response['Vary'] = 'Origin'
    else:
        response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Credentials'] = 'true'
    return response
