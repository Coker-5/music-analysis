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
      cdata: []
    }
  },
  components: { Chart },
  async mounted() {
    const res = await this.$request.get("music/centerLeft2/")
    this.cdata = res.data
  }
}
</script>
