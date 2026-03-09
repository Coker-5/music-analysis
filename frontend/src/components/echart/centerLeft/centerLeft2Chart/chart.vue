<template>
  <div>
    <Echart
      id="centreLeft2Chart"
      :options="options"
      height="360px"
      width="330px"
    ></Echart>
  </div>
</template>

<script>
import Echart from '@/common/echart';
export default {
  data() {
    return {
      options: {}
    };
  },
  components: { Echart },
  props: {
    cdata: {
      type: Array,
      default: () => []
    }
  },
  watch: {
    cdata: {
      handler(newData) {
        if (!newData || newData.length === 0) return
        this.options = {
          backgroundColor: 'transparent',
          series: [{
            type: 'wordCloud',
            shape: 'circle',
            left: 'center',
            top: 'center',
            width: '90%',
            height: '90%',
            right: null,
            bottom: null,
            sizeRange: [14, 60],
            rotationRange: [-45, 45],
            rotationStep: 15,
            gridSize: 8,
            drawOutOfBound: false,
            textStyle: {
              fontFamily: 'sans-serif',
              fontWeight: 'bold',
              color: function () {
                const colors = [
                  '#37a2da', '#32c5e9', '#9fe6b8',
                  '#ffdb5c', '#ff9f7f', '#fb7293',
                  '#e7bcf3', '#8378ea', '#00bcd4'
                ]
                return colors[Math.floor(Math.random() * colors.length)]
              }
            },
            emphasis: {
              focus: 'self',
              textStyle: { shadowBlur: 10, shadowColor: '#333' }
            },
            data: newData
          }]
        }
      },
      immediate: true,
      deep: true
    }
  }
};
</script>
