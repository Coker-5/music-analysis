from rest_framework.routers import SimpleRouter
from apps.music.views import (
    DimSingerViewSet, DimWeekIssueViewSet,
    FactWeeklyChartViewSet, FactDailyChartViewSet,
    AggSingerTotalViewSet, AggSongLongevityViewSet,
)

router = SimpleRouter()
router.register('singer',        DimSingerViewSet,        basename='singer')
router.register('week-issue',    DimWeekIssueViewSet,     basename='week-issue')
router.register('weekly-chart',  FactWeeklyChartViewSet,  basename='weekly-chart')
router.register('daily-chart',   FactDailyChartViewSet,   basename='daily-chart')
router.register('singer-stat',   AggSingerTotalViewSet,   basename='singer-stat')
router.register('song-longevity',AggSongLongevityViewSet, basename='song-longevity')

urlpatterns = router.urls
