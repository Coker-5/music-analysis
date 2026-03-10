from __future__ import annotations
from django.db import models


class DimSinger(models.Model):
    singer_id   = models.CharField(primary_key=True, max_length=50, verbose_name='歌手ID')
    singer_name = models.CharField(max_length=100, verbose_name='歌手名称')
    created_at  = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        managed    = True
        db_table   = 'dim_singer'
        verbose_name = '歌手信息'

    def __str__(self):
        return self.singer_name


class DimWeekIssue(models.Model):
    issue        = models.IntegerField(primary_key=True, verbose_name='期数编号')
    month        = models.CharField(max_length=20, verbose_name='月份')
    start_date   = models.DateField(null=True, blank=True, verbose_name='开始日期')
    end_date     = models.DateField(null=True, blank=True, verbose_name='结束日期')
    title        = models.CharField(max_length=100, verbose_name='标题')
    publish_time = models.DateTimeField(null=True, blank=True, verbose_name='发布时间')

    class Meta:
        managed    = False
        db_table   = 'dim_week_issue'
        verbose_name = '周榜期数'
        ordering   = ['-issue']

    def __str__(self):
        return f"第{self.issue}期 {self.title}"


class FactWeeklyChart(models.Model):
    id          = models.AutoField(primary_key=True)
    issue       = models.IntegerField(verbose_name='周榜期数')
    rank        = models.IntegerField(verbose_name='排名')
    song_id     = models.CharField(max_length=50, verbose_name='歌曲ID')
    song_name   = models.CharField(max_length=200, verbose_name='歌曲名称')
    singer_id   = models.CharField(max_length=50, verbose_name='歌手ID')
    singer_name = models.CharField(max_length=100, verbose_name='歌手名称')
    uni_index   = models.DecimalField(max_digits=8, decimal_places=2, null=True, verbose_name='综合指数')
    new_flag    = models.BooleanField(default=False, verbose_name='是否新入榜')
    cover_image = models.TextField(null=True, blank=True, verbose_name='封面图URL')

    class Meta:
        managed     = False
        db_table    = 'fact_weekly_chart'
        verbose_name = '历史周榜'
        ordering    = ['-issue', 'rank']

    def __str__(self):
        return f"[第{self.issue}期 #{self.rank}] {self.song_name}"


class FactDailyChart(models.Model):
    id            = models.AutoField(primary_key=True)
    chart_date    = models.DateField(verbose_name='榜单日期')
    rank          = models.IntegerField(verbose_name='排名')
    song_id       = models.CharField(max_length=50, verbose_name='歌曲ID')
    song_name     = models.CharField(max_length=200, verbose_name='歌曲名称')
    singer_id     = models.CharField(max_length=50, null=True, blank=True, verbose_name='歌手ID')
    singer_name   = models.CharField(max_length=100, verbose_name='歌手名称')
    score         = models.DecimalField(max_digits=8, decimal_places=2, null=True, verbose_name='得分')
    incr_rank     = models.IntegerField(default=0, verbose_name='排名变化')
    incr_score    = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name='得分变化')
    play_index    = models.DecimalField(max_digits=8, decimal_places=2, null=True, verbose_name='播放指数')
    pay_index     = models.DecimalField(max_digits=8, decimal_places=2, null=True, verbose_name='畅销指数')
    pop_index     = models.DecimalField(max_digits=8, decimal_places=2, null=True, verbose_name='人气指数')
    days_on_chart = models.IntegerField(default=0, verbose_name='上榜天数')
    new_flag      = models.BooleanField(default=False, verbose_name='是否新入榜')
    track_tags    = models.JSONField(null=True, blank=True, verbose_name='标签')
    cover_image   = models.TextField(null=True, blank=True, verbose_name='封面图URL')

    class Meta:
        managed     = False
        db_table    = 'fact_daily_chart'
        verbose_name = '今日日榜'
        ordering    = ['-chart_date', 'rank']

    def __str__(self):
        return f"[{self.chart_date} #{self.rank}] {self.song_name}"


class AggSingerTotal(models.Model):
    singer_id      = models.CharField(primary_key=True, max_length=50, verbose_name='歌手ID')
    singer_name    = models.CharField(max_length=100, verbose_name='歌手名称')
    total_count    = models.IntegerField(default=0, verbose_name='总上榜次数')
    champion_count = models.IntegerField(default=0, verbose_name='夺冠次数')
    top3_count     = models.IntegerField(default=0, verbose_name='Top3次数')
    last_updated   = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        managed     = False
        db_table    = 'agg_singer_total'
        verbose_name = '歌手统计'
        ordering    = ['-total_count']

    def __str__(self):
        return f"{self.singer_name}（{self.total_count}次）"


class AggSongLongevity(models.Model):
    song_id           = models.CharField(primary_key=True, max_length=50, verbose_name='歌曲ID')
    song_name         = models.CharField(max_length=200, verbose_name='歌曲名称')
    singer_name       = models.CharField(max_length=100, verbose_name='歌手名称')
    total_weeks       = models.IntegerField(default=0, verbose_name='总留榜周数')
    champion_weeks    = models.IntegerField(default=0, verbose_name='夺冠周数')
    history_best_rank = models.IntegerField(null=True, blank=True, verbose_name='历史最好排名')
    cover_image       = models.TextField(null=True, blank=True, verbose_name='封面图URL')

    class Meta:
        managed     = False
        db_table    = 'agg_song_longevity'
        verbose_name = '歌曲留榜'
        ordering    = ['-total_weeks']

    def __str__(self):
        return f"{self.song_name}（{self.total_weeks}周）"
