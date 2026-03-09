<template>
  <div id="centerRight1">
    <div class="bg-color-black">
      <div class="d-flex pt-2 pl-2">
        <span>
          <icon name="chart-line" class="text-icon"></icon>
        </span>
        <div class="d-flex">
          <span class="fs-xl text mx-2">长红歌曲留榜排行</span>
        </div>
      </div>
      <div class="d-flex jc-center body-box">
        <dv-scroll-board
          class="dv-scr-board"
          :config="config"
          :key="config.data.length"
        />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      config: {
        header: ['歌曲', '歌手', '留榜周', '最高名'],
        data: [['加载中', '--', '--', '--']],
        rowNum: 7,
        headerHeight: 35,
        headerBGC: '#0f1325',
        oddRowBGC: '#0f1325',
        evenRowBGC: '#171c33',
        index: true,
        columnWidth: [50, 80, 60, 50, 50],
        align: ['center']
      }
    }
  },
  async mounted() {
    const res = await this.$request.get("music/centerRight2/")
    const longevity = res.data.longevity_top8 || []
    this.config.data = longevity.map(item => [
      item.song_name,
      item.singer_name,
      item.total_weeks + '周',
      'No.' + item.history_best_rank
    ])
  }
}
</script>

<style lang="scss" scoped>
$box-height: 410px;
$box-width: 300px;
#centerRight1 {
  padding: 16px;
  padding-top: 20px;
  height: $box-height;
  width: $box-width;
  border-radius: 5px;
  .bg-color-black {
    height: $box-height - 30px;
    border-radius: 10px;
  }
  .text {
    color: #c3cbde;
  }
  .body-box {
    border-radius: 10px;
    overflow: hidden;
    .dv-scr-board {
      width: 270px;
      height: 340px;
    }
  }
}
</style>
