<template>
  <div id="bottomRight">
    <div class="bg-color-black">
      <div class="d-flex pt-2 pl-2">
        <span>
          <icon name="chart-area" class="text-icon"></icon>
        </span>
        <div class="d-flex">
          <span class="fs-xl text mx-2">音乐榜单 Top200</span>
          <div class="decoration2">
            <dv-decoration-2 :reverse="true" style="width:5px;height:6rem;"/>
          </div>
        </div>
      </div>
      <div class="row-list">
        <ul class="music-rank" style="width:100%;height:420px;overflow:auto">
          <li class="header-row">
            <div>排名</div>
            <div>封面</div>
            <div>歌曲信息</div>
            <div>今日得分</div>
            <div>得分变化</div>
            <div>排名变化</div>
            <div>上榜天数</div>
            <div>标签</div>
          </li>
          <li v-for="song in songs" :key="song.rank">
            <div class="rank-num">{{ song.rank }}</div>
            <div>
              <img :src="song.cover_image" :alt="song.song_name" style="height:50px;width:50px;border-radius:4px;">
            </div>
            <div class="song-info">
              <p class="song-name">{{ song.song_name }}</p>
              <p class="singer-name">{{ song.singer_name }}</p>
            </div>
            <div class="score-col">{{ song.score }}</div>
            <div :class="song.incr_score >= 0 ? 'colorGrass' : 'colorRed'">
              {{ song.incr_score >= 0 ? '+' + song.incr_score : song.incr_score }}
            </div>
            <div :class="song.incr_rank > 0 ? 'colorGrass' : song.incr_rank < 0 ? 'colorRed' : ''">
              <span v-if="song.incr_rank > 0">↑{{ song.incr_rank }}</span>
              <span v-else-if="song.incr_rank < 0">↓{{ Math.abs(song.incr_rank) }}</span>
              <span v-else>—</span>
            </div>
            <div>{{ song.days_on_chart }}天</div>
            <div class="tags-col">
              <span
                v-for="(tag, i) in (song.track_tags || []).slice(0,2)"
                :key="i"
                class="tag-item"
              >{{ tag }}</span>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      songs: []
    }
  },
  async mounted() {
    const res = await this.$request.get("music/bottomLeft/")
    this.songs = res.data
  }
}
</script>

<style lang="scss">
$box-height: 520px;
$box-width: 100%;

#bottomRight {
  padding: 14px 16px;
  height: $box-height;
  width: $box-width;
  border-radius: 5px;

  .bg-color-black {
    height: $box-height - 30px;
    border-radius: 10px;
  }
  .text { color: #c3cbde; }
  .decoration2 {
    position: absolute;
    right: 0.125rem;
  }

  .row-list {
    .music-rank::-webkit-scrollbar { display: none; }

    .music-rank li {
      display: grid;
      grid-template-columns: 50px 60px 160px 80px 80px 80px 80px 1fr;
      cursor: pointer;
      margin-left: 16px;
      text-align: center;
      line-height: 60px;
      border-bottom: 1px solid rgba(255,255,255,0.05);
    }

    .header-row {
      font-size: 14px;
      color: #67e0e3;
      line-height: 36px !important;
      border-bottom: 1px solid rgba(103,224,227,0.3) !important;
    }

    .rank-num {
      font-size: 18px;
      font-weight: bold;
      color: #ffdb5c;
    }

    .song-info {
      text-align: left;
      line-height: 1.4;
      display: flex;
      flex-direction: column;
      justify-content: center;
      .song-name {
        color: #ffffff;
        font-size: 14px;
        margin: 0;
      }
      .singer-name {
        color: #9ca3b3;
        font-size: 12px;
        margin: 0;
      }
    }

    .score-col { color: #32c5e9; font-weight: bold; }
    .colorGrass { color: #9fe6b8; }
    .colorRed { color: #fb7293; }

    .tags-col {
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      gap: 4px;
      line-height: 1;
      .tag-item {
        background: rgba(50,197,233,0.15);
        border: 1px solid rgba(50,197,233,0.4);
        color: #32c5e9;
        font-size: 11px;
        padding: 2px 6px;
        border-radius: 10px;
      }
    }
  }
}
</style>
