<template>
  <div class="system-predict-container layout-padding" id="id" v-loading="state.loading">
    <div class="system-predict-padding layout-padding-auto layout-padding-view">
      <!-- Socket连接状态指示器 -->
      <div class="socket-status-indicator" :class="socketStatus">
        <div class="status-dot"></div>
        <span class="status-text">{{ socketStatusText }}</span>
      </div>
      
      <div class="carousel">
        <div class="section-title"><i></i><span>课堂行为检测</span></div>
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
            @change="(val) => { console.log('思考模式切换:', val) }"
          />
        </div>
        <div class="conf" style="margin-left: 20px;display: flex; flex-direction: row;">
          <div style="font-size: 14px;margin-right: 20px;display: flex;justify-content: start;align-items: center;color: #909399;">
            设置最小置信度阈值
          </div>
          <el-slider v-model="conf" :format-tooltip="formatTooltip" style="width: 300px;" />
        </div>
        <div class="button-section" style="margin-left: 20px">
          <el-button type="primary" @click="upData" class="predict-button">开始检测</el-button>
        </div>
        <div class="button-section" style="margin-left: 20px">
          <el-button type="primary" @click="() => htmlToPDF('id', '课堂行为检测报告')" class="predict-button">PDF导出</el-button>
        </div>
      </div>
      <div style="width: 100%; height: 350px; display: flex; flex-direction: row; justify-content: center; align-items: center; margin-bottom: 20px;">
        <el-card shadow="hover" class="card">
          <el-upload v-model="state.img" ref="uploadFile" class="avatar-uploader"
            action="/dev-api/files/upload" :show-file-list="false" 
            :on-success="handleAvatarSuccessone"
            :on-error="handleUploadError">
            <img v-if="imageUrl" :src="imageUrl" class="avatar" />
            <el-icon v-else class="avatar-uploader-icon">
              <Plus />
            </el-icon>
          </el-upload>
        </el-card>
        <el-card class="result-section" v-if="state.predictionResult.label">
          <div class="bottom">
            <div class="result-content">
              <el-card shadow="never" class="info-card">
                <div class="info-item">
                  <div class="info-label">
                    <el-icon class="icon"><Select /></el-icon>
                    <span>识别结果</span>
                  </div>
                  <div class="info-value highlight">{{ state.predictionResult.label || '-' }}</div>
                </div>

                <div class="info-item">
                  <div class="info-label">
                    <el-icon class="icon"><Opportunity /></el-icon>
                    <span>检测概率</span>
                  </div>
                  <div class="info-value accent">{{ state.predictionResult.confidence || '-' }}</div>
                </div>

                <div class="info-item">
                  <div class="info-label">
                    <el-icon class="icon"><Clock /></el-icon>
                    <span>总耗时</span>
                  </div>
                  <div class="info-value">{{ state.predictionResult.allTime ? `${state.predictionResult.allTime}` : '-' }}</div>
                </div>
              </el-card>
            </div>
            <div style="width: 100%; margin-top: 20px;">
              <h4>详细结果</h4>
              <el-table :data="state.data" style="width: 100%">
                <el-table-column prop="label" label="检测结果" align="center" />
                <el-table-column prop="confidence" label="置信度" align="center" />
                <el-table-column prop="allTime" label="总用时" align="center" />
              </el-table>
            </div>
          </div>
        </el-card>
      </div>
      <div class="carousel">
        <div class="section-title"><i></i><span>AI建议</span></div>
      </div>
      <div style="width: 100%;margin-bottom: 20px; padding: 0 300px;">
        <div v-if="state.predictionResult.suggestion" style="width:100%;padding: 20px 100px; border-radius: 10px;min-height: 50px;border: 1px solid #ccc">
          <div v-html="state.predictionResult.suggestion" class="markdown-body"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup name="ImgPredict">
import { reactive, ref, onMounted, onUnmounted, computed } from 'vue';
import { ElMessage } from 'element-plus';
import request from '@/utils/request';
import { Plus, Select, Clock, Opportunity } from '@element-plus/icons-vue';
import useUserStore from '@/store/modules/user';
import { parseTime } from '@/utils/ruoyi';
import { marked } from 'marked';
import { io } from 'socket.io-client';

const imageUrl = ref('');
const ai = ref('');
const conf = ref(25);
const weight = ref('');
const thinkMode = ref(false);
const uploadFile = ref();
const userStore = useUserStore();

// Socket连接状态
const socketConnected = ref(false);
const socketConnecting = ref(true);
let socket = null;

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
  img: '',
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
    { value: 'Qwen3.0-LAN', label: '使用Qwen3.0（局域网）' },
    { value: 'Qwen2.5-VL-LAN', label: '使用Qwen2.5-VL（局域网）' },
    { value: 'Qwen2.5-Omni-LAN', label: '使用Qwen2.5-Omni（局域网）' },
    { value: 'Gemma3-LAN', label: '使用Gemma3（局域网）' },
    { value: 'Deepseek-R1-Local', label: '使用Deepseek-R1（本地）' },
    { value: 'Qwen3.0-Local', label: '使用Qwen3.0（本地）' },
    { value: 'Qwen2.5-VL-Local', label: '使用Qwen2.5-VL（本地）' },
    { value: 'Qwen2.5-Omni-Local', label: '使用Qwen2.5-Omni（本地）' },
    { value: 'Gemma3-Local', label: '使用Gemma3（本地）' },
    { value: '不使用AI', label: '不使用大模型' },
  ],
  form: {
    username: '',
    inputImg: null,
    weight: '',
    conf: null,
    ai: '',
    thinkMode: false,
    startTime: ''
  },
});

const formatTooltip = (val) => {
  return val / 100
}

const handleAvatarSuccessone = (response, uploadFile) => {
  console.log('=== 文件上传成功回调 ===');
  console.log('完整响应对象:', JSON.stringify(response, null, 2));
  console.log('uploadFile:', uploadFile);
  
  // 检查响应格式
  if (!response) {
    ElMessage.error('上传响应为空');
    return;
  }
  
  // 检查响应码
  if (response.code && response.code !== 200) {
    ElMessage.error(response.msg || '上传失败');
    console.error('上传失败，错误信息:', response.msg);
    return;
  }
  
  // 显示上传的图片预览
  imageUrl.value = URL.createObjectURL(uploadFile.raw);
  
  // 提取文件路径（按优先级尝试不同字段）
  let imgPath = '';
  
  // 1. 尝试从 data 字段获取（这是RuoYi标准格式）
  if (response.data) {
    if (typeof response.data === 'string') {
      imgPath = response.data;
    } else if (response.data.url) {
      imgPath = response.data.url;
    } else if (response.data.fileName) {
      imgPath = response.data.fileName;
    }
  }
  
  // 2. 尝试直接从 url 字段获取
  if (!imgPath && response.url) {
    imgPath = response.url;
  }
  
  // 3. 尝试从 msg 字段获取（某些情况下URL会被放在这里）
  if (!imgPath && response.msg && typeof response.msg === 'string' && response.msg.startsWith('http')) {
    imgPath = response.msg;
  }
  
  // 4. 尝试从 fileName 字段获取
  if (!imgPath && response.fileName) {
    imgPath = response.fileName;
  }
  
  // 5. 如果响应本身就是字符串
  if (!imgPath && typeof response === 'string') {
    imgPath = response;
  }
  
  if (!imgPath) {
    console.error('无法从响应中提取文件路径');
    console.error('响应结构:', response);
    ElMessage.error('图片上传成功，但无法获取文件路径');
    return;
  }
  
  state.img = imgPath;
  console.log('✅ 成功设置图片路径:', state.img);
  ElMessage.success('图片上传成功');
};

const handleUploadError = (error, uploadFile) => {
  console.error('=== 文件上传失败 ===');
  console.error('错误信息:', error);
  console.error('文件信息:', uploadFile);
  ElMessage.error('图片上传失败：' + (error.message || '未知错误'));
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

const transformData = (rawData) => {
  return rawData.label.map((label, index) => ({
    allTime: rawData.allTime,
    confidence: rawData.confidence[index],
    label: label,
  }));
}

const upData = () => {
  console.log('开始检测，当前state.img值:', state.img);
  console.log('state.img类型:', typeof state.img);
  console.log('state.img是否为空:', !state.img);
  
  if (!state.img) {
    ElMessage.error('请先上传图片！');
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

  state.loading = true;
  state.form.weight = weight.value;
  state.form.conf = (parseFloat(conf.value) / 100);
  state.form.username = userStore.name || 'admin';
  state.form.inputImg = state.img;
  state.form.ai = ai.value;
  
  if (ai.value === 'Qwen3.0-Local' || ai.value === 'Qwen3.0-LAN' || 
      ai.value === 'Qwen2.5-VL-Local' || ai.value === 'Qwen2.5-VL-LAN') {
    state.form.thinkMode = thinkMode.value === true;
  } else {
    state.form.thinkMode = false;
  }
  
  state.form.startTime = parseTime(new Date(), '{y}-{m}-{d} {h}:{i}:{s}');
  
  const requestData = {
    ...state.form,
    thinkMode: state.form.thinkMode
  };
  
  request.post('/flask/predict', requestData).then((res) => {
    console.log('=== 检测接口响应 ===');
    console.log('完整响应:', res);
    
    if (res.code == 200) {
      try {
        state.loading = false;
        
        // 第一步：解析 Flask 返回的 JSON 字符串
        console.log('原始 res.data 类型:', typeof res.data);
        console.log('原始 res.data 内容:', res.data);
        
        const parsedData = typeof res.data === 'string' ? JSON.parse(res.data) : res.data;
        console.log('解析后的数据:', parsedData);
        
        // 第二步：处理 label 和 confidence（它们可能是数组或JSON字符串）
        state.predictionResult.label = Array.isArray(parsedData.label) 
          ? parsedData.label 
          : JSON.parse(parsedData.label);
        
        state.predictionResult.confidence = Array.isArray(parsedData.confidence)
          ? parsedData.confidence
          : JSON.parse(parsedData.confidence);
        
        state.predictionResult.allTime = parsedData.allTime;
        state.predictionResult.suggestion = marked(parsedData.suggestion || '暂无建议');
        
        console.log('处理后的检测结果:', state.predictionResult);
        
        // 第三步：转换数据用于表格显示
        state.data = transformData(state.predictionResult);
        
        // 🔥 关键：更新图片显示为检测结果的可视化图
        if (parsedData.outImg) {
          console.log('✅ 更新可视化图:', parsedData.outImg);
          imageUrl.value = parsedData.outImg;
        } else {
          console.warn('⚠️ Flask未返回 outImg 字段');
        }
        
        ElMessage.success('检测成功！');
      } catch (error) {
        console.error('❌ 解析检测结果时出错:', error);
        console.error('错误堆栈:', error.stack);
        ElMessage.error('解析检测结果失败：' + error.message);
      }
    } else {
      state.loading = false;
      ElMessage.error(res.msg || '检测失败');
    }
  }).catch((error) => {
    console.error('❌ 检测接口调用失败:', error);
    state.loading = false;
    ElMessage.error('检测失败：' + (error.message || '网络错误'));
  });
};

const htmlToPDF = (elementId, filename) => {
  // 使用浏览器原生打印功能导出PDF
  window.print();
};

// 初始化Socket连接
const initSocket = () => {
  socket = io('http://127.0.0.1:5000', {
    transports: ['polling', 'websocket'],  // 先使用polling，再升级到websocket
    reconnection: true,
    reconnectionAttempts: 5,
    reconnectionDelay: 1000
  });

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

.markdown-body {
  line-height: 1.6;
  font-size: 16px;
}

.markdown-body pre {
  background: #f4f4f4;
  padding: 10px;
  border-radius: 5px;
  overflow-x: auto;
}

.markdown-body code {
  background: #f4f4f4;
  padding: 2px 5px;
  border-radius: 3px;
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

.card {
  width: 100%;
  height: 100%;
  border-radius: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.avatar-uploader .avatar {
  width: 100%;
  height: 280px;
  display: block;
  object-fit: contain;
}

.el-icon.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 100%;
  height: 280px;
  text-align: center;
  line-height: 280px;
}

.button-section {
  display: flex;
  justify-content: center;
}

.predict-button {
  background: #9E87FF;
  width: 100%;
}

.result-section {
  width: 50%;
  height: 100%;
  margin-left: 15px;
  text-align: center;
  display: flex;
  flex-direction: column;
  border-radius: 6px;
}

.bottom {
  width: 100%;
  font-size: 18px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.result-content {
  width: 100%;
  margin-top: 16px;

  .info-card {
    padding: 20px;
    border-radius: 8px;
    background: #f8f9fa;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.06);
  }

  .info-item {
    margin: 12px 0;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    padding: 8px 0;
    border-bottom: 1px solid #eee;

    &:last-child {
      border-bottom: none;
    }

    .info-label {
      display: flex;
      align-items: center;
      color: #606266;
      font-size: 14px;

      .icon {
        margin-right: 8px;
        font-size: 16px;
        color: #409eff;
      }
    }

    .info-value {
      font-size: 16px;
      font-weight: 500;
      color: #303133;
      flex: 1;
      margin-left: 16px;

      &.highlight {
        color: #67c23a;
        font-weight: 600;
      }

      &.accent {
        color: #e6a23c;
      }
    }
  }
}
</style>
