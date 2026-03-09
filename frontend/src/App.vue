<template>
  <div id="app">
    <router-view />
    <!-- 移动端提示遮罩层 -->
    <div v-if="showMobileWarning" class="mobile-warning">
      <div class="warning-content">
        <h3>移动端访问提示</h3>
        <p>建议使用PC端浏览器访问，以获得更好的体验</p>
        <button class="confirm-btn" @click="closeWarning">继续访问</button>
      </div>
    </div>


  </div>
</template>


<script>
export default {
  name: 'App',
  data() {
    return {
      showMobileWarning: false
    }
  },
  mounted() {
    this.checkDevice();
  },
  methods: {
    // 设备检测
    isMobileDevice() {
      const userAgent = navigator.userAgent.toLowerCase();
      const mobileKeywords = ['android', 'iphone', 'ipod', 'blackberry', 'windows phone', 'opera mini', 'iemobile', 'mobile'];
      return mobileKeywords.some(keyword => userAgent.includes(keyword));
    },
    
    // 检查设备并决定是否显示提示
    checkDevice() {
      // 如果是非移动设备，不显示
      if (!this.isMobileDevice()) return;

        // 延迟显示，避免与页面渲染冲突
        setTimeout(() => {
          this.showMobileWarning = true;
        }, 1000);
      
    },
    
    // 关闭提示
    closeWarning() {
      const today = new Date().toDateString();
      localStorage.setItem('mobileWarningClosed', today);
      this.showMobileWarning = false;
    }
  }
}
</script>

<style lang="scss" scoped>
#app {
  width: 100vw;
  height: 100vh;
  background-color: #020308;
  overflow: hidden;
}

.mobile-warning {
  position: fixed;
  inset: 0; // 等价于 top: 0; right: 0; bottom: 0; left: 0;
  background: rgba(0, 0, 0, 0.7);
  z-index: 9999;
  display: flex;
  justify-content: center; // 水平居中
  align-items: center; // 垂直居中
  padding: 20px; // 添加内边距，防止内容紧贴屏幕边缘
}

.warning-content {
  background: white;
  width: 80%;
  max-width: 400px;
  border-radius: 10px;
  padding: 20px;
  text-align: center;
  box-shadow: 0 4px 20px rgba(0,0,0,0.15);
}

.warning-content h3 {
  margin-top: 10px;
  margin-bottom: 10px;
  color: #333;
  font-size: 20px;
}

.warning-content p {
  color: #666;
  font-size: 16px;
  line-height: 1.6;
}

.warning-icon {
  font-size: 50px;
}

.confirm-btn {
  background: #4a90e2;
  color: white;
  border: none;
  padding: 10px 25px;
  font-size: 16px;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 15px;
  transition: background 0.3s;
}

.confirm-btn:hover {
  background: #3a7bc8;
}
</style>


