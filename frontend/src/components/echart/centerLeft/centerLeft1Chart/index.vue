<template>
  <div>
    <Chart :cdata="cdata" />
  </div>
</template>

<script>
import Chart from './chart.vue';
export default {
  data() {
    return {
      cdata: {
        xData: [],
        seriesData: []
      }
    }
  },
  components: { Chart },
  async mounted() {
    const res = await this.$request.get("music/centerLeft1/")
    const data = res.data
    this.cdata = {
      xData: data.map(item => item.singer_name),
      seriesData: data.map(item => ({
        name: item.singer_name,
        value: item.total_count
      }))
    }
  }
}
</script>
