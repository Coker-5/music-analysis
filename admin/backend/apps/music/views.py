from rest_framework.permissions import AllowAny
from dvadmin.utils.filters import CoreModelFilterBankend
from dvadmin.utils.viewset import CustomModelViewSet
from apps.music.models import (
    DimSinger, DimWeekIssue, FactWeeklyChart,
    FactDailyChart, AggSingerTotal, AggSongLongevity
)
from apps.music.serializers import (
    DimSingerSerializer, DimWeekIssueSerializer,
    FactWeeklyChartSerializer, FactDailyChartSerializer,
    AggSingerTotalSerializer, AggSongLongevitySerializer
)


class DimSingerViewSet(CustomModelViewSet):
    queryset         = DimSinger.objects.all()
    serializer_class = DimSingerSerializer
    search_fields    = ['singer_name', 'singer_id']
    ordering_fields  = ['singer_id']
    permission_classes = [AllowAny]
    # Avoid data-level permission filters for public datasets
    extra_filter_class = [CoreModelFilterBankend]


class DimWeekIssueViewSet(CustomModelViewSet):
    queryset         = DimWeekIssue.objects.all()
    serializer_class = DimWeekIssueSerializer
    search_fields    = ['title', 'month']
    ordering_fields  = ['-issue']
    permission_classes = [AllowAny]
    extra_filter_class = []


class FactWeeklyChartViewSet(CustomModelViewSet):
    queryset         = FactWeeklyChart.objects.all()
    serializer_class = FactWeeklyChartSerializer
    search_fields    = ['song_name', 'singer_name']
    filterset_fields = ['issue', 'rank', 'singer_id', 'new_flag', 'song_name', 'singer_name']
    ordering_fields  = ['-issue', 'rank']
    permission_classes = [AllowAny]
    extra_filter_class = []


class FactDailyChartViewSet(CustomModelViewSet):
    queryset         = FactDailyChart.objects.all()
    serializer_class = FactDailyChartSerializer
    search_fields    = ['song_name', 'singer_name']
    filterset_fields = ['chart_date', 'rank', 'new_flag', 'song_name', 'singer_name']
    ordering_fields  = ['-chart_date', 'rank']
    permission_classes = [AllowAny]
    extra_filter_class = []


class AggSingerTotalViewSet(CustomModelViewSet):
    queryset         = AggSingerTotal.objects.all()
    serializer_class = AggSingerTotalSerializer
    search_fields    = ['singer_name']
    ordering_fields  = ['-total_count']
    permission_classes = [AllowAny]
    extra_filter_class = []


class AggSongLongevityViewSet(CustomModelViewSet):
    queryset         = AggSongLongevity.objects.all()
    serializer_class = AggSongLongevitySerializer
    search_fields    = ['song_name', 'singer_name']
    ordering_fields  = ['-total_weeks']
    permission_classes = [AllowAny]
    extra_filter_class = []
