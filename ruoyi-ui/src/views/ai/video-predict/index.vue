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
        <div class="weight">
          <el-select v-model="ai" placeholder="请选择AI助手" size="large" style="margin-left: 20px;width: 200px" @change="getData">
            <el-option v-for="item in state.ai_items" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </div>
        <div v-if="ai && (ai === 'Qwen3.0-Local' || ai === 'Qwen3.0-LAN')" style="margin-left: 20px;">
          <el-switch
            v-model="thinkMode"
            active-text="思考模式"
            inactive-text="非思考模式"
            style="margin-top: 5px;"
          />
        </div>
        <div class="conf" style="margin-left: 20px;display: flex; flex-direction: row;">
          <div style="font-size: 14px;margin-right: 20px;display: flex;justify-content: start;align-items: center;color: #909399;">
            设置最小置信度阈值
          </div>
          <el-slider v-model="conf" :format-tooltip="formatTooltip" style="width: 300px;" />
        </div>
        <el-upload v-model="state.form.inputVideo" ref="uploadFile" class="avatar-uploader"
          action="/dev-api/files/upload" :show-file-list="false" 
          :on-success="handleAvatarSuccessone"
          :on-error="handleUploadError">
          <div class="button-section" style="margin-left: 20px">
            <el-button type="info" class="predict-button">上传视频</el-button>
          </div>
        </el-upload>
        <div class="button-section" style="margin-left: 20px">
          <el-button type="primary" @click="upData" class="predict-button">开始处理</el-button>
        </div>
        <div class="demo-progress" v-if="state.isShow">
          <el-progress :text-inside="true" :stroke-width="20" :percentage="state.percentage" style="width: 400px;">
            <span>{{ state.type_text }} {{ state.percentage }}%</span>
          </el-progress>
        </div>
      </div>
      
      <!-- 视频检测结果 -->
      <div class="section-title"><i></i><span>检测结果</span></div>
      <div class="result-section">
        <div class="cards" ref="cardsContainer">
          <!-- 处理完成后显示最终视频 -->
          <video v-if="state.final_video_url" class="video" :src="state.final_video_url" controls>
            您的浏览器不支持视频播放
          </video>
          <!-- 处理过程中显示流式图像 -->
          <img v-else-if="state.video_path" class="video" :src="state.video_path" alt="实时检测画面">
          <!-- 未开始检测 -->
          <div v-else class="no-result">尚未有检测结果</div>
        </div>
      </div>
      
      <!-- AI建议部分 -->
      <div class="carousel">
        <div class="section-title"><i></i><span>AI建议</span></div>
      </div>
      <div style="width: 100%;margin-bottom: 50px;">
        <div v-if="state.predictionResult.suggestion" 
             style="width:100%;padding: 20px; border-radius: 10px;min-height: 200px;border: 1px solid #ccc; max-height: 600px; overflow-y: auto;">
          <div v-html="state.predictionResult.suggestion" class="markdown-body"></div>
        </div>
        <div v-else-if="ai && ai !== '不使用AI'" 
             style="width:100%;padding: 20px; border-radius: 10px;min-height: 50px;border: 1px dashed #ccc; text-align: center; color: #909399;">
          尚未生成AI建议
        </div>
        <div v-else 
             style="width:100%;padding: 20px; border-radius: 10px;min-height: 50px;border: 1px dashed #ccc; text-align: center; color: #909399;">
          未使用AI助手
        </div>
      </div>
    </div>
  </div>
</template>

<script setup name="VideoPredict">
import { reactive, ref, onMounted, onUnmounted, computed } from 'vue';
import { ElMessage } from 'element-plus';
import request from '@/utils/request';
import useUserStore from '@/store/modules/user';
import { parseTime } from '@/utils/ruoyi';
import { marked } from 'marked';
import { io } from 'socket.io-client';

const uploadFile = ref();
const userStore = useUserStore();
const conf = ref(25);
const weight = ref('');
const ai = ref('');
const thinkMode = ref(false);

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
  loading: false,
  weight_items: [],
  video_path: '',
  final_video_url: '',  // 🔥 新增：存储处理完成后的最终视频URL
  data: [],
  predictionResult: {
    label: '',
    confidence: '',
    allTime: '',
    suggestion: ''
  },
  ai_items: [
    { value: 'Deepseek-R1', label: '使用Deepseek-R1' },
    { value: 'Qwen', label: '使用Qwen' },
    { value: 'Deepseek-R1-LAN', label: '使用Deepseek-R1（局域网）' },
    { value: 'Qwen3.0-LAN', label: '使用qwen3.0（局域网）' },
    { value: 'Qwen2.5-VL-LAN', label: '使用qwen2.5-VL（局域网）' },
    { value: 'Qwen2.5-Omni-LAN', label: '使用Qwen2.5-Omni（局域网）' },
    { value: 'Gemma3-LAN', label: '使用Gemma3（局域网）' },
    { value: 'Deepseek-R1-Local', label: '使用Deepseek-R1（本地）' },
    { value: 'Qwen3.0-Local', label: '使用qwen3.0（本地）' },
    { value: 'Qwen2.5-VL-Local', label: '使用qwen2.5-VL（本地）' },
    { value: 'Qwen2.5-Omni-Local', label: '使用Qwen2.5-Omni（本地）' },
    { value: 'Gemma3-Local', label: '使用Gemma3（本地）' },
    { value: '不使用AI', label: '不使用大模型' },
  ],
  form: {
    username: '',
    inputVideo: null,
    weight: '',
    conf: null,
    ai: '',
    thinkMode: false,
    startTime: ''
  },
  type_text: "正在保存",
  percentage: 50,
  isShow: false,
});

let socket = null;

const handleAvatarSuccessone = (response, uploadFile) => {
  console.log('=== 视频上传成功回调 ===');
  console.log('完整响应对象:', JSON.stringify(response, null, 2));
  
  if (!response) {
    ElMessage.error('上传响应为空');
    return;
  }
  
  if (response.code && response.code !== 200) {
    ElMessage.error(response.msg || '上传失败');
    console.error('上传失败，错误信息:', response.msg);
    return;
  }
  
  // 提取文件路径
  let videoPath = '';
  if (response.data) {
    if (typeof response.data === 'string') {
      videoPath = response.data;
    } else if (response.data.url) {
      videoPath = response.data.url;
    } else if (response.data.fileName) {
      videoPath = response.data.fileName;
    }
  } else if (response.url) {
    videoPath = response.url;
  } else if (response.msg && typeof response.msg === 'string' && response.msg.startsWith('http')) {
    videoPath = response.msg;
  } else if (response.fileName) {
    videoPath = response.fileName;
  } else if (typeof response === 'string') {
    videoPath = response;
  }
  
  if (!videoPath) {
    console.error('无法从响应中提取视频路径');
    console.error('响应结构:', response);
    ElMessage.error('视频上传成功，但无法获取文件路径');
    return;
  }
  
  state.form.inputVideo = videoPath;
  console.log('✅ 成功设置视频路径:', state.form.inputVideo);
  ElMessage.success('视频上传成功');
};

const handleUploadError = (error, uploadFile) => {
  console.error('=== 视频上传失败 ===');
  console.error('错误信息:', error);
  console.error('文件信息:', uploadFile);
  ElMessage.error('视频上传失败：' + (error.message || '未知错误'));
};

const formatTooltip = (val) => {
  return val / 100;
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

const initSocket = () => {
  if (!socket) {
    socket = io('http://127.0.0.1:5000', {
      transports: ['websocket', 'polling'],
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

    socket.on('suggestion', (data) => {
      try {
        state.predictionResult.suggestion = marked(data);
        // AI建议已成功生成并显示
      } catch (error) {
        console.error('处理建议时出错:', error);
        state.predictionResult.suggestion = data;
      }
    });

    // 🔥 新增：监听视频处理完成事件
    socket.on('video_complete', (data) => {
      console.log('=== 收到视频处理完成事件 ===');
      console.log('最终视频URL:', data.url || data);
      
      const videoUrl = data.url || data;
      if (videoUrl) {
        state.final_video_url = videoUrl;
        console.log('✅ 已设置最终视频URL，页面将显示可播放的视频');
        ElMessage.success('视频处理完成！');
      }
    });
  }
};

const upData = () => {
  if (!state.form.inputVideo) {
    ElMessage.error('请先上传视频文件！');
    return;
  }
  if (!weight.value) {
    ElMessage.error('请选择检测模型！');
    return;
  }
  if (!ai.value) {
    ElMessage.error('请选择AI助手！');
    return;
  }
  
  initSocket();
  
  state.loading = true;
  state.form.weight = weight.value;
  state.form.conf = (parseFloat(conf.value) / 100);
  state.form.username = userStore.name || 'admin';
  state.form.ai = ai.value;
  state.form.thinkMode = thinkMode.value;
  state.form.startTime = parseTime(new Date(), '{y}-{m}-{d} {h}:{i}:{s}');
  
  const queryParams = new URLSearchParams();
  Object.keys(state.form).forEach(key => {
    if (state.form[key] !== null && state.form[key] !== undefined) {
      queryParams.append(key, state.form[key]);
    }
  });
  
  // 🔥 清空之前的最终视频URL，开始新的检测
  state.final_video_url = '';
  state.video_path = `http://127.0.0.1:5000/predictVideo?${queryParams.toString()}`;
  
  state.predictionResult.suggestion = '';
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

.predict-button {
  background: #9E87FF;
  width: 100%;
}

.system-predict-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: auto;

  .system-predict-padding {
    padding: 0 100px;
    overflow-y: auto;

    .el-table {
      flex: 1;
    }
  }
}

.header {
  width: 100%;
  height: 5%;
  display: flex;
  justify-content: start;
  align-items: center;
  font-size: 20px;
}

.result-section {
  margin-top: 15px;
  margin-bottom: 30px;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.cards {
  width: 100%;
  border-radius: 5px;
  padding: 20px;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  max-height: 600px;
}

.no-result {
  width: 100%;
  height: 300px;
  display: flex;
  justify-content: center;
  align-items: center;
  border: 1px dashed #ccc;
  color: #909399;
}

.video {
  max-width: 80%;
  max-height: 600px;
  height: auto;
  width: auto;
  object-fit: contain;
  margin: 0 auto;
  display: block;
}

.button-section {
  display: flex;
  justify-content: center;
}

.demo-progress .el-progress--line {
  margin-left: 20px;
  width: 600px;
}

.carousel {
  width: 100%;

  .section-title {
    margin-bottom: 50px;
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

.markdown-body {
  line-height: 1.6;
  font-size: 16px;

  h1, h2, h3, h4, h5, h6 {
    margin-top: 24px;
    margin-bottom: 16px;
    font-weight: 600;
    line-height: 1.25;
  }

  h1 {
    font-size: 2em;
    padding-bottom: 0.3em;
    border-bottom: 1px solid #eaecef;
  }

  h2 {
    font-size: 1.5em;
    padding-bottom: 0.3em;
    border-bottom: 1px solid #eaecef;
  }

  h3 {
    font-size: 1.25em;
  }

  p, ul, ol {
    margin-top: 0;
    margin-bottom: 16px;
  }

  ul, ol {
    padding-left: 2em;
  }

  li + li {
    margin-top: 0.25em;
  }

  pre {
    background: #f6f8fa;
    padding: 16px;
    border-radius: 5px;
    overflow-x: auto;
    margin-bottom: 16px;
  }

  code {
    background: #f6f8fa;
    padding: 3px 6px;
    border-radius: 3px;
    font-family: monospace;
  }

  blockquote {
    padding: 0 1em;
    color: #6a737d;
    border-left: 0.25em solid #dfe2e5;
    margin: 0 0 16px 0;
  }
}
</style>
