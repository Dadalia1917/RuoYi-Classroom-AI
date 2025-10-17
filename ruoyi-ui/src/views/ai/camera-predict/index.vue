<template>
  <div class="system-predict-container layout-padding">
    <div class="system-predict-padding layout-padding-auto layout-padding-view">
      <!-- Socket连接状态指示器 -->
      <div class="socket-status-indicator" :class="socketStatus">
        <div class="status-dot"></div>
        <span class="status-text">{{ socketStatusText }}</span>
      </div>
      
      <div class="header">
        <div class="weight">
          <el-select v-model="weight" placeholder="请选择模型" size="large" style="width: 200px">
            <el-option v-for="item in state.weight_items" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </div>
        <div class="conf" style="margin-left: 20px;display: flex; flex-direction: row;">
          <div style="font-size: 14px;margin-right: 20px;display: flex;justify-content: start;align-items: center;color: #909399;">
            设置最小置信度阈值
          </div>
          <el-slider v-model="conf" :format-tooltip="formatTooltip" style="width: 300px;" />
        </div>
        <div class="button-section" style="margin-left: 20px">
          <el-button type="primary" @click="start" class="predict-button">开始录制</el-button>
        </div>
        <div class="button-section" style="margin-left: 20px">
          <el-button type="primary" @click="stop" class="predict-button">结束录制</el-button>
        </div>
        <div class="demo-progress" v-if="state.isShow">
          <el-progress :text-inside="true" :stroke-width="20" :percentage="state.percentage" style="width: 400px;">
            <span>{{ state.type_text }} {{ state.percentage }}%</span>
          </el-progress>
        </div>
      </div>
      
      <!-- 实时检测画面 -->
      <div class="section-title" v-if="state.cameraisShow || state.final_video_url"><i></i><span>{{ state.final_video_url ? '检测结果' : '实时检测' }}</span></div>
      <div class="cards" ref="cardsContainer">
        <!-- 录制完成后显示最终视频 -->
        <video v-if="state.final_video_url" class="video" :src="state.final_video_url" controls>
          您的浏览器不支持视频播放
        </video>
        <!-- 录制过程中显示流式图像 -->
        <img v-else-if="state.cameraisShow" class="video" :src="state.video_path" alt="实时检测画面">
        <!-- 未开始检测 -->
        <div v-else class="no-result">
          <el-icon class="no-result-icon"><VideoCamera /></el-icon>
          <p>点击"开始录制"开始摄像头检测</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup name="CameraPredict">
import { reactive, ref, onMounted, onUnmounted, computed } from 'vue';
import { ElMessage } from 'element-plus';
import request from '@/utils/request';
import useUserStore from '@/store/modules/user';
import { parseTime } from '@/utils/ruoyi';
import { VideoCamera } from '@element-plus/icons-vue';
import { io } from 'socket.io-client';

const userStore = useUserStore();
const conf = ref(25);
const weight = ref('');

// Socket连接状态
const socketConnected = ref(false);
const socketConnecting = ref(true);

// 计算属性：连接状态样式类
const socketStatus = computed(() => {
  if (socketConnected.value) return 'connected';
  if (socketConnecting.value) return 'connecting';
  return 'disconnected';
});

// 计算属性：连接状态文本
const socketStatusText = computed(() => {
  if (socketConnected.value) return 'Flask服务已连接';
  if (socketConnecting.value) return '正在连接Flask服务...';
  return 'Flask服务未连接';
});

const state = reactive({
  weight_items: [],
  data: {},
  video_path: '',
  final_video_url: '',  // 🔥 新增：存储录制完成后的最终视频URL
  type_text: "正在保存",
  percentage: 50,
  isShow: false,
  cameraisShow: false,
  form: {
    username: '',
    weight: '',
    conf: null,
    startTime: ''
  },
});

let socket = null;

const formatTooltip = (val) => {
  return val / 100;
};

const initSocket = () => {
  if (!socket) {
    socket = io('http://127.0.0.1:5000', {
      transports: ['polling', 'websocket'],  // 先使用polling，再升级到websocket
      reconnection: true,
      reconnectionAttempts: 5,
      reconnectionDelay: 1000
    });
    
    // 连接状态监听
    socket.on('connect', () => {
      console.log('Socket连接成功');
      socketConnected.value = true;
      socketConnecting.value = false;
    });

    socket.on('connect_error', (err) => {
      console.error('Socket连接错误:', err);
      socketConnected.value = false;
      socketConnecting.value = false;
    });

    socket.on('disconnect', (reason) => {
      console.log('Socket断开连接:', reason);
      socketConnected.value = false;
      socketConnecting.value = false;
    });

    // 业务事件监听
    socket.on('message', (data) => {
      console.log('Received message:', data);
      // 不再显示弹窗提示，使用右上角状态指示器即可
    });

    socket.on('progress', (data) => {
      state.percentage = parseInt(data);
      if (parseInt(data) < 100) {
        state.isShow = true;
      } else {
        // 保存完成，隐藏进度条
        setTimeout(() => {
          state.isShow = false;
          state.percentage = 0;
        }, 2000);
      }
    });

    // 🔥 新增：监听视频处理完成事件
    socket.on('video_complete', (data) => {
      console.log('=== 收到摄像头录制完成事件 ===');
      console.log('最终视频URL:', data.url || data);
      
      const videoUrl = data.url || data;
      if (videoUrl) {
        state.final_video_url = videoUrl;
        state.cameraisShow = false;  // 停止显示流式图像
        console.log('✅ 已设置最终视频URL，页面将显示可播放的视频');
        ElMessage.success('录制完成！');
      }
    });
  }
};

const getData = () => {
  request.get('/flask/file_names').then((res) => {
    console.log('获取模型列表响应:', res);
    if (res.code == 200) {
      try {
        console.log('原始数据:', res.data);
        // res 已经是 { code, msg, data } 对象，res.data 是 Flask 返回的 JSON 字符串
        const parsedData = JSON.parse(res.data);
        console.log('解析后数据:', parsedData);
        state.weight_items = parsedData.weight_items;
        console.log('模型列表:', state.weight_items);
      } catch (error) {
        console.error('解析JSON失败:', error, '原始数据:', res.data);
        ElMessage.error('解析模型列表数据失败！');
      }
    } else {
      ElMessage.error(res.msg);
    }
  }).catch((error) => {
    console.error('获取模型列表失败:', error);
    ElMessage.error('获取模型列表失败：' + error.message);
  });
};

const start = () => {
  if (!weight.value) {
    ElMessage.error('请选择检测模型！');
    return;
  }
  
  initSocket();
  
  state.form.weight = weight.value;
  state.form.conf = (parseFloat(conf.value) / 100);
  state.form.username = userStore.name || 'admin';
  state.form.startTime = parseTime(new Date(), '{y}-{m}-{d} {h}:{i}:{s}');
  
  // 🔥 清空之前的最终视频URL，开始新的录制
  state.final_video_url = '';
  
  const queryParams = new URLSearchParams(state.form).toString();
  state.cameraisShow = true;
  state.video_path = `http://127.0.0.1:5000/predictCamera?${queryParams}`;
};

const stop = () => {
  request.get('/flask/stopCamera').then((res) => {
    if (res.code !== 200) {
      ElMessage.error(res.msg || '停止录制失败！');
    }
  }).catch(() => {
    ElMessage.error('停止录制失败！');
  });
  
  state.cameraisShow = false;
};

onMounted(() => {
  getData();
  initSocket();
});

onUnmounted(() => {
  if (socket) {
    socket.disconnect();
    socket = null;
  }
});
</script>

<style scoped lang="scss">
// Socket连接状态指示器样式
.socket-status-indicator {
  position: fixed;
  top: 70px;
  right: 20px;
  display: flex;
  align-items: center;
  padding: 8px 16px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  transition: all 0.3s ease;

  .status-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    margin-right: 8px;
    animation: pulse 2s infinite;
  }

  .status-text {
    font-size: 14px;
    font-weight: 500;
  }

  &.connected {
    .status-dot {
      background: #67c23a;
      box-shadow: 0 0 0 0 rgba(103, 194, 58, 0.4);
    }
    .status-text {
      color: #67c23a;
    }
  }

  &.connecting {
    .status-dot {
      background: #e6a23c;
      box-shadow: 0 0 0 0 rgba(230, 162, 60, 0.4);
    }
    .status-text {
      color: #e6a23c;
    }
  }

  &.disconnected {
    .status-dot {
      background: #f56c6c;
      box-shadow: 0 0 0 0 rgba(245, 108, 108, 0.4);
    }
    .status-text {
      color: #f56c6c;
    }
  }
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 currentColor;
  }
  70% {
    box-shadow: 0 0 0 8px rgba(0, 0, 0, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(0, 0, 0, 0);
  }
}

.system-predict-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;

  .system-predict-padding {
    padding: 15px;

    .el-table {
      flex: 1;
    }
  }
}

.predict-button {
  background: #9E87FF;
  width: 100%;
}

.header {
  width: 100%;
  height: 5%;
  display: flex;
  justify-content: start;
  align-items: center;
  font-size: 20px;
  margin-bottom: 20px;
}

.cards {
  width: 100%;
  height: 80vh;
  border-radius: 5px;
  margin-top: 15px;
  padding: 0px;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #f5f5f5;
}

.no-result {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: #909399;
  font-size: 16px;
  
  .no-result-icon {
    font-size: 48px;
    margin-bottom: 16px;
  }
  
  p {
    margin: 0;
  }
}

.video {
  width: 100%;
  max-height: 100%;
  height: auto;
  object-fit: contain;
}

.button-section {
  display: flex;
  justify-content: center;
}

.demo-progress .el-progress--line {
  margin-left: 20px;
  width: 600px;
}

.section-title {
  margin-bottom: 20px;
  font-size: 20px;
  text-align: center;
  position: relative;
  padding: 20px 0;
  display: flex;
  justify-content: center;
  justify-items: center;

  i {
    background: #9E87FF;
    height: 1px;
    width: 100%;
    position: absolute;
    top: 40px;
  }

  span {
    background: #9E87FF;
    line-height: 40px;
    position: absolute;
    width: 120px;
    left: 50%;
    margin-left: -60px;
    color: #fff;
  }
}
</style>
