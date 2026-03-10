from rest_framework import serializers
from dvadmin.utils.serializers import CustomModelSerializer
from apps.music.models import (
    DimSinger, DimWeekIssue, FactWeeklyChart,
    FactDailyChart, AggSingerTotal, AggSongLongevity
)


class DimSingerSerializer(CustomModelSerializer):
    class Meta:
        model  = DimSinger
        fields = '__all__'
        read_only_fields = ['singer_id', 'created_at']


class DimWeekIssueSerializer(CustomModelSerializer):
    class Meta:
        model  = DimWeekIssue
        fields = '__all__'
        read_only_fields = ['issue']


class FactWeeklyChartSerializer(CustomModelSerializer):
    class Meta:
        model  = FactWeeklyChart
        fields = '__all__'
        read_only_fields = ['id']


class FactDailyChartSerializer(CustomModelSerializer):
    class Meta:
        model  = FactDailyChart
        fields = '__all__'
        read_only_fields = ['id']


class AggSingerTotalSerializer(CustomModelSerializer):
    class Meta:
        model  = AggSingerTotal
        fields = '__all__'
        read_only_fields = ['singer_id']


class AggSongLongevitySerializer(CustomModelSerializer):
    class Meta:
        model  = AggSongLongevity
        fields = '__all__'
        read_only_fields = ['song_id']
