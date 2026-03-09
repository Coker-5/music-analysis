<template>
  <div id="app">
    <div ref="chartContainer" style="width:100%;height:460px;"></div>
  </div>
</template>

<script>
import Highcharts from 'highcharts';
import Highcharts3D from 'highcharts/highcharts-3d';
Highcharts3D(Highcharts);

export default {
  name: 'SingerEvolutionChart',
  data() {
    return {
      chart: null
    }
  },
  async mounted() {
    this.chart = Highcharts.chart(this.$refs.chartContainer, {
      chart: {
        type: 'column',
        options3d: {
          enabled: true,
          alpha: 10,
          beta: 30,
          depth: 100,
          viewDistance: 25,
        },
        backgroundColor: 'rgba(19, 25, 47, 0.6)'
      },
      title: {
        text: '歌手历年上榜次数演化',
        style: { color: '#ffffff' }
      },
      xAxis: {
        categories: [],
        labels: { style: { color: '#ffffff' } }
      },
      yAxis: {
        title: { text: '上榜周次', style: { color: '#ffffff' } },
        labels: { style: { color: '#ffffff' } }
      },
      legend: {
        enabled: true,
        itemStyle: { color: '#ffffff' }
      },
      tooltip: {
        headerFormat: '<b>{point.key}年</b><br>',
        pointFormat: '{series.name}: <b>{point.y}</b> 周'
      },
      plotOptions: {
        column: {
          depth: 25,
          groupZPadding: 10
        }
      },
      series: []
    })

    const res = await this.$request.get("music/bottomRight/")
    const data = res.data

    this.chart.xAxis[0].setCategories(data.years.map(String))

    data.series.forEach(s => {
      this.chart.addSeries({
        name: s.singer,
        data: s.data
      }, false)
    })

    this.chart.redraw()
  },
  beforeDestroy() {
    if (this.chart) {
      this.chart.destroy()
      this.chart = null
    }
  }
}
</script>

<style>
#app {
  width: 100%;
  height: 100%;
}
</style>
