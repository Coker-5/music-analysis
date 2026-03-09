<template>
  <div class="progress-bar-container">
    <div class="progress-bar-text" ref="progressBarText"></div>
    <div ref="progressBarInner" class="progress-bar-inner"></div>
  </div>
</template>

<script>
import ProgressBar from 'progressbar.js';

export default {
  data() {
    return {
      bar: null,
    };
  },
  mounted() {
    this.bar = new ProgressBar.Line(this.$refs.progressBarInner, {
      strokeWidth: 8,
      color: '#257dff',
      trailColor: '#e0e0e0',
      trailWidth: 8,
      duration: 3300,
      easing: 'easeInOut',
      step: (state, bar) => {
        const percent = Math.round(bar.value() * 100);
        this.$refs.progressBarText.innerText = "Loading...：" + percent + '%';
      },
    });

    this.bar.animate(1);
  },
  beforeDestroy() {
    this.bar.destroy();
  },
};
</script>

<style scoped>
.progress-bar-container {
  position: relative;
  width: 60%;
  height: 40px; /* 设置容器高度 */
  background-color: #e0e0e0;
  border-radius: 15px;
  top:47%;
  left:20%
}

.progress-bar-text {
  position: absolute;
  top: -33px; /* 将文本提升到进度条上方 */
  left: 52%;
  transform: translateX(-50%);
  color: #fff;
  font-size: 1.5rem;
  white-space: nowrap; /* 防止文本换行 */
}

.progress-bar-inner {
  height: 100%; /* 填满容器 */
  border-radius: 15px; /* 保持圆角 */
  overflow: hidden; /* 避免溢出 */
}
</style>
