import Vue from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import dataV from '@jiaminghi/data-view';
// 引入全局css
import './assets/scss/style.scss';
import $request from '@/api/request';
// 按需引入vue-awesome图标
import Icon from 'vue-awesome/components/Icon';
import 'vue-awesome/icons/chart-bar.js';
import 'vue-awesome/icons/chart-area.js';
import 'vue-awesome/icons/chart-pie.js';
import 'vue-awesome/icons/chart-line.js';
import 'vue-awesome/icons/align-left.js';


//引入 echarts
import * as echarts from 'echarts'
import 'echarts-wordcloud'
Vue.prototype.$echarts = echarts
Vue.config.productionTip = false;
Vue.prototype.$request = $request

// 全局注册
Vue.component('icon', Icon);
Vue.use(dataV);

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount('#app');
