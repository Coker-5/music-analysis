<template>
  <div id="center">
    <div class="up">
      <div class="bg-color-black item">
        <p class="ml-3 colorBlue fw-b fs-xl">今日冠军歌曲</p>
        <span class="dv-dig-flop ml-1 mt-2 pl-3 fzl">{{ headData.champion_song }}</span>
      </div>
      <div class="bg-color-black item">
        <p class="ml-3 colorBlue fw-b fs-xl">今日冠军歌手</p>
        <span class="dv-dig-flop ml-1 mt-2 pl-3 fzl">{{ headData.champion_singer }}</span>
      </div>
      <div class="bg-color-black item">
        <p class="ml-3 colorBlue fw-b fs-xl">今日平均得分</p>
        <span class="dv-dig-flop ml-1 mt-2 pl-3 fzl">{{ headData.avg_score }}</span>
      </div>
      <div class="bg-color-black item">
        <p class="ml-3 colorBlue fw-b fs-xl">Top10新入榜</p>
        <span class="dv-dig-flop ml-1 mt-2 pl-3 fzl">{{ headData.top10_new_count + '首' }}</span>
      </div>
      <div class="bg-color-black item">
        <p class="ml-3 colorBlue fw-b fs-xl">今日最大涨幅</p>
        <span class="dv-dig-flop ml-1 mt-2 pl-3 fzl">{{ headData.max_incr_song }}</span>
      </div>
      <div class="bg-color-black item">
        <p class="ml-3 colorBlue fw-b fs-xl">涨幅名次</p>
        <span class="dv-dig-flop ml-1 mt-2 pl-3 fzl">{{ '+' + headData.max_incr_value }}</span>
      </div>
    </div>

    <div class="down">
      <div class="ranking bg-color-black">
        <span>
          <icon name="chart-bar" class="text-icon"></icon>
        </span>
        <span class="fs-xl text mx-2 mb-1 pl-3">歌手上榜次数排行</span>
        <dv-scroll-ranking-board
          class="dv-scr-rank-board mt-1"
          v-bind:config="ranking"
          v-if="ranking.data.length > 0"
          v-bind:key="ranking.data[0].value"
        />
      </div>

      <div class="percent">
        <div class="item bg-color-black">
          <span>播放指数</span>
          <CenterChart
            :id="rate[0].id"
            :tips="rate[0].tips"
            :colorObj="rate[0].colorData"
          />
        </div>
        <div class="item bg-color-black">
          <span>畅销指数</span>
          <CenterChart
            :id="rate[1].id"
            :tips="rate[1].tips"
            :colorObj="rate[1].colorData"
          />
        </div>
        <div class="item bg-color-black">
          <span>人气指数</span>
          <CenterChart
            :id="rate[2].id"
            :tips="rate[2].tips"
            :colorObj="rate[2].colorData"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import CenterChart from '@/components/echart/center/centerChartRate'

export default {
  data() {
    return {
      headData: {
        champion_song: '--',
        champion_singer: '--',
        avg_score: '--',
        top10_new_count: 0,
        max_incr_song: '--',
        max_incr_value: 0,
      },
      ranking: {
        data: [{ name: '加载中', value: 0 }],
        carousel: 'single',
        unit: '次'
      },
      rate: [
        {
          id: 'centerRate1',
          tips: 0,
          colorData: {
            textStyle: '#3fc0fb',
            series: {
              color: ['#00bcd44a', 'transparent'],
              dataColor: { normal: '#03a9f4', shadowColor: '#97e2f5' }
            }
          }
        },
        {
          id: 'centerRate2',
          tips: 0,
          colorData: {
            textStyle: '#67e0e3',
            series: {
              color: ['#faf3a378', 'transparent'],
              dataColor: { normal: '#ff9800', shadowColor: '#fcebad' }
            }
          }
        },
        {
          id: 'centerRate3',
          tips: 0,
          colorData: {
            textStyle: '#fb7293',
            series: {
              color: ['#fb729378', 'transparent'],
              dataColor: { normal: '#fb7293', shadowColor: '#f9b4c3' }
            }
          }
        }
      ]
    }
  },
  async mounted() {
    const headRes = await this.$request.get("music/head/")
    this.headData = headRes.data

    const centerRes = await this.$request.get("music/centerData/")
    const centerData = centerRes.data
    const rankData = centerData.singers.map((name, i) => ({
      name: name,
      value: centerData.counts[i]
    }))
    this.$set(this.ranking, 'data', rankData)

    const indexRes = await this.$request.get("music/centerRight1/")
    const indexData = indexRes.data
    this.rate[0].tips = Math.round(indexData.play_index)
    this.rate[1].tips = Math.round(indexData.pay_index)
    this.rate[2].tips = Math.round(indexData.pop_index)
  },
  components: {
    CenterChart
  }
}
</script>

<style lang="scss" scoped>
.fzl {
  font-size: larger;
  line-height: 2;
  padding-left: 2rem;
}

#center {
  display: flex;
  flex-direction: column;

  .up {
    width: 100%;
    display: flex;
    flex-wrap: wrap;
    justify-content: space-around;

    .item {
      border-radius: 6px;
      padding-top: 8px;
      margin-top: 8px;
      width: 32%;
      height: 70px;

      .dv-dig-flop {
        width: 150px;
        height: 30px;
      }
    }
  }

  .down {
    padding: 6px 4px;
    padding-bottom: 0;
    width: 100%;
    display: flex;
    height: 255px;
    justify-content: space-between;

    .bg-color-black {
      border-radius: 5px;
    }

    .ranking {
      padding: 10px;
      width: 59%;

      .dv-scr-rank-board {
        height: 225px;
      }
    }

    .percent {
      width: 40%;
      display: flex;
      flex-wrap: wrap;

      .item {
        width: 50%;
        height: 120px;

        span {
          margin-top: 8px;
          font-size: 14px;
          display: flex;
          justify-content: center;
        }
      }
    }
  }
}
</style>
