<template>
  <div id="centerRight2">
    <div class="bg-color-black">
      <div class="d-flex pt-2 pl-2">
        <span>
          <icon name="align-left" class="text-icon"></icon>
        </span>
        <span class="fs-xl text mx-2">今日得分区间分布</span>
      </div>
      <div class="d-flex ai-center flex-column body-box">
        <dv-capsule-chart
          class="dv-cap-chart"
          :config="capsuleConfig"
          :key="capsuleConfig.data.length"
        />
        <div class="stat-info">
          <p class="colorBlue">今日榜单共 {{ totalCount }} 首</p>
          <p style="color:#9fe6b8">得分范围 {{ minScore }} ~ {{ maxScore }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      totalCount: 0,
      minScore: 0,
      maxScore: 0,
      capsuleConfig: {
        data: [{ name: '加载中', value: 0 }],
        colors: ['#e062ae', '#fb7293', '#e690d1', '#32c5e9', '#96bfff'],
        unit: '首',
        showValue: true
      }
    }
  },
  async mounted() {
    const res = await this.$request.get("music/centerRight2/")
    const dist = res.data.score_distribution || []
    this.capsuleConfig.data = dist.map(item => ({
      name: item.range + '分',
      value: item.count
    }))
    this.totalCount = dist.reduce((sum, item) => sum + item.count, 0)
    this.minScore = 60
    this.maxScore = 100
  }
}
</script>

<style lang="scss" scoped>
#centerRight2 {
  $box-height: 410px;
  $box-width: 340px;
  padding: 5px;
  height: $box-height;
  width: $box-width;
  border-radius: 5px;
  .bg-color-black {
    padding: 5px;
    height: $box-height;
    width: $box-width;
    border-radius: 10px;
  }
  .text { color: #c3cbde; }
  .body-box {
    border-radius: 10px;
    overflow: hidden;
    .dv-cap-chart {
      width: 100%;
      height: 260px;
      margin-top: 10px;
    }
  }
  .stat-info {
    width: 100%;
    padding: 8px 16px;
    p { font-size: 13px; margin: 4px 0; }
  }
}
</style>
