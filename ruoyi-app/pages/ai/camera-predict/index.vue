<template>
  <view class="camera-predict-container">
    <!-- 连接状态指示器 -->
    <view class="status-indicator" :class="connectionStatus">
      <view class="status-dot"></view>
      <text class="status-text">{{ statusText }}</text>
    </view>
    
    <!-- 实时检测画面区域 -->
    <view class="detection-section">
      <view class="section-header">
        <text class="section-title">{{ finalVideoUrl ? '检测结果' : (isDetecting ? '实时检测中' : '摄像头检测') }}</text>
      </view>
      
      <view class="video-box">
        <!-- 录制完成后显示最终视频 -->
        <video 
          v-if="finalVideoUrl" 
          :src="finalVideoUrl" 
          class="result-video"
          controls
          objectFit="contain"
        ></video>
        
        <!-- 检测过程中显示流式图像 -->
        <image 
          v-else-if="isDetecting && streamUrl" 
          :src="streamUrl" 
          class="stream-image"
          mode="aspectFit"
        ></image>
        
        <!-- 未开始检测 -->
        <view v-else class="placeholder">
          <text class="placeholder-icon">📹</text>
          <text class="placeholder-text">点击"开始录制"开始摄像头检测</text>
        </view>
      </view>
    </view>
    
    <!-- 模型选择 -->
    <view class="config-section">
      <view class="config-item">
        <text class="config-label">选择模型</text>
        <picker mode="selector" :range="modelOptions" range-key="name" @change="onModelChange" :disabled="isDetecting">
          <view class="picker-box">
            <text class="picker-text">{{ selectedModel.name || '请选择模型' }}</text>
            <text class="picker-arrow">▼</text>
          </view>
        </picker>
      </view>
      
      <view class="config-item">
        <text class="config-label">置信度阈值</text>
        <view class="slider-box">
          <slider 
            :value="confidence" 
            min="0" 
            max="100" 
            @change="onConfidenceChange"
            activeColor="#007aff"
            backgroundColor="#e9ecef"
            block-color="#007aff"
            :disabled="isDetecting"
          />
          <text class="slider-value">{{ (confidence / 100).toFixed(2) }}</text>
        </view>
      </view>
    </view>
    
    <!-- 控制按钮 -->
    <view class="control-buttons">
      <view 
        class="control-btn start-btn" 
        :class="{ disabled: !selectedModel.value || isDetecting }"
        @click="startDetection"
      >
        <text class="btn-text">开始录制</text>
      </view>
      
      <view 
        class="control-btn stop-btn" 
        :class="{ disabled: !isDetecting }"
        @click="stopDetection"
      >
        <text class="btn-text">结束录制</text>
      </view>
    </view>
    
    <!-- AI建议部分 -->
    <view v-if="aiSuggestion" class="suggestion-section">
      <view class="section-header">
        <text class="section-title">AI教学建议</text>
      </view>
      <view class="suggestion-box">
        <rich-text :nodes="aiSuggestion"></rich-text>
      </view>
    </view>
    
    <!-- 进度条 -->
    <view v-if="showProgress" class="progress-section">
      <progress 
        :percent="progress" 
        :show-info="true"
        stroke-width="12"
        activeColor="#007aff"
      />
      <text class="progress-text">{{ progressText }} {{ progress }}%</text>
    </view>
  </view>
</template>

<script>
import { getModelList, stopCamera } from '@/api/ai/predict'
import config from '@/config.js'
import { useUserStore } from '@/store/modules/user'

export default {
  data() {
    return {
      // 连接状态
      connectionStatus: 'disconnected', // connected, connecting, disconnected
      
      // 检测状态
      isDetecting: false,
      streamUrl: '',
      finalVideoUrl: '',
      
      // 配置
      modelOptions: [],
      selectedModel: {},
      confidence: 25,
      
      // AI建议
      aiSuggestion: '',
      
      // 进度
      showProgress: false,
      progress: 0,
      progressText: '正在处理',
      
      // 定时器
      progressTimer: null,
      connectionCheckTimer: null
    }
  },
  computed: {
    statusText() {
      const statusMap = {
        'connected': 'Flask服务已连接',
        'connecting': '正在连接...',
        'disconnected': 'Flask服务未连接'
      }
      return statusMap[this.connectionStatus] || '未知状态'
    },
    username() {
      const userStore = useUserStore()
      return userStore.name || 'admin'
    }
  },
  onLoad() {
    this.fetchModelList()
    this.checkConnection()
  },
  onShow() {
    if (this.modelOptions.length === 0) {
      this.fetchModelList()
    }
  },
  onUnload() {
    this.cleanup()
  },
  onHide() {
    // 页面隐藏时停止检测
    if (this.isDetecting) {
      this.stopDetection()
    }
  },
  methods: {
    // 检查Flask连接状态
    checkConnection() {
      this.connectionStatus = 'connecting'
      
      uni.request({
        url: config.baseUrl + '/flask/file_names',
        method: 'GET',
        timeout: 5000,
        success: (res) => {
          if (res.statusCode === 200) {
            this.connectionStatus = 'connected'
          } else {
            this.connectionStatus = 'disconnected'
          }
        },
        fail: () => {
          this.connectionStatus = 'disconnected'
        }
      })
      
      // 定期检查连接状态
      this.connectionCheckTimer = setInterval(() => {
        if (!this.isDetecting) {
          this.checkConnection()
        }
      }, 10000) // 每10秒检查一次
    },
    
    // 获取模型列表
    fetchModelList() {
      const defaultModels = [
        { name: 'best.pt', value: 'best.pt' },
        { name: 'yolov8n.pt', value: 'yolov8n.pt' },
        { name: 'RT-DETR.pt', value: 'RT-DETR.pt' }
      ]
      
      getModelList().then(response => {
        try {
          let data = response.data
          if (typeof data === 'string') {
            data = JSON.parse(data)
          }
          
          const weightItems = data.weight_items || data
          this.modelOptions = weightItems.map(item => ({
            name: item.label || item.value || item,
            value: item.value || item
          }))
          
          if (this.modelOptions.length > 0) {
            this.selectedModel = this.modelOptions[0]
          }
        } catch (error) {
          console.error('解析模型列表失败:', error)
          this.modelOptions = defaultModels
          this.selectedModel = defaultModels[0]
        }
      }).catch(error => {
        console.error('获取模型列表失败:', error)
        this.modelOptions = defaultModels
        this.selectedModel = defaultModels[0]
        
        uni.showToast({
          title: '使用默认模型',
          icon: 'none',
          duration: 2000
        })
      })
    },
    
    // 开始检测
    startDetection() {
      if (!this.selectedModel.value) {
        uni.showToast({
          title: '请选择检测模型',
          icon: 'none'
        })
        return
      }
      
      if (this.isDetecting) {
        return
      }
      
      // 检查连接状态
      if (this.connectionStatus !== 'connected') {
        uni.showToast({
          title: 'Flask服务未连接',
          icon: 'none',
          duration: 2000
        })
        return
      }
      
      this.isDetecting = true
      this.finalVideoUrl = ''
      this.aiSuggestion = ''
      
      // 构建请求参数
      const params = {
        username: this.username,
        weight: this.selectedModel.value,
        conf: this.confidence / 100,
        startTime: new Date().toISOString().replace('T', ' ').substring(0, 19)
      }
      
      const queryString = Object.keys(params)
        .map(key => `${key}=${encodeURIComponent(params[key])}`)
        .join('&')
      
      // 设置流式图像URL（Flask的MJPEG stream）
      // 添加时间戳防止缓存
      this.streamUrl = `http://127.0.0.1:5000/predictCamera?${queryString}&t=${Date.now()}`
      
      console.log('开始摄像头检测，流URL:', this.streamUrl)
      
      uni.showToast({
        title: '开始录制',
        icon: 'success'
      })
      
      // 模拟进度更新（因为无法获取实际进度）
      this.startProgressSimulation()
    },
    
    // 停止检测
    stopDetection() {
      if (!this.isDetecting) {
        return
      }
      
      uni.showLoading({
        title: '正在停止...'
      })
      
      // 调用后端停止接口
      stopCamera().then(response => {
        console.log('停止录制响应:', response)
        
        this.isDetecting = false
        this.streamUrl = ''
        
        uni.hideLoading()
        uni.showToast({
          title: '录制已停止',
          icon: 'success'
        })
        
        // 停止进度模拟
        if (this.progressTimer) {
          clearInterval(this.progressTimer)
          this.progressTimer = null
        }
        
        // 显示保存进度
        this.showProgress = true
        this.progress = 0
        this.progressText = '正在保存视频'
        
        // 模拟保存进度
        const saveInterval = setInterval(() => {
          this.progress += 10
          if (this.progress >= 100) {
            clearInterval(saveInterval)
            this.progress = 100
            
            // 2秒后隐藏进度条
            setTimeout(() => {
              this.showProgress = false
              this.progress = 0
              
              // TODO: 这里应该从后端获取最终视频URL
              // this.finalVideoUrl = response.videoUrl
              
              uni.showToast({
                title: '视频已保存',
                icon: 'success'
              })
            }, 2000)
          }
        }, 200)
        
      }).catch(error => {
        console.error('停止录制失败:', error)
        uni.hideLoading()
        uni.showToast({
          title: '停止失败',
          icon: 'none'
        })
        
        // 强制停止
        this.isDetecting = false
        this.streamUrl = ''
        
        if (this.progressTimer) {
          clearInterval(this.progressTimer)
          this.progressTimer = null
        }
      })
    },
    
    // 模拟进度更新
    startProgressSimulation() {
      this.showProgress = true
      this.progress = 10
      this.progressText = '正在检测'
      
      this.progressTimer = setInterval(() => {
        if (this.progress < 90) {
          this.progress += Math.random() * 5
          if (this.progress > 90) {
            this.progress = 90
          }
        }
      }, 1000)
    },
    
    // 选择模型
    onModelChange(e) {
      const index = e.detail.value
      this.selectedModel = this.modelOptions[index]
    },
    
    // 调整置信度
    onConfidenceChange(e) {
      this.confidence = e.detail.value
    },
    
    // 清理资源
    cleanup() {
      if (this.isDetecting) {
        this.stopDetection()
      }
      
      if (this.progressTimer) {
        clearInterval(this.progressTimer)
        this.progressTimer = null
      }
      
      if (this.connectionCheckTimer) {
        clearInterval(this.connectionCheckTimer)
        this.connectionCheckTimer = null
      }
    }
  }
}
</script>

<style scoped>
.camera-predict-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 30rpx;
}

/* 连接状态指示器 */
.status-indicator {
  position: fixed;
  top: 20rpx;
  right: 20rpx;
  display: flex;
  align-items: center;
  padding: 16rpx 24rpx;
  border-radius: 40rpx;
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.15);
  z-index: 1000;
}

.status-dot {
  width: 16rpx;
  height: 16rpx;
  border-radius: 50%;
  margin-right: 12rpx;
  animation: pulse 2s infinite;
}

.status-text {
  font-size: 24rpx;
  font-weight: 500;
}

.status-indicator.connected .status-dot {
  background: #67c23a;
}

.status-indicator.connected .status-text {
  color: #67c23a;
}

.status-indicator.connecting .status-dot {
  background: #e6a23c;
}

.status-indicator.connecting .status-text {
  color: #e6a23c;
}

.status-indicator.disconnected .status-dot {
  background: #f56c6c;
}

.status-indicator.disconnected .status-text {
  color: #f56c6c;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

/* 检测画面区域 */
.detection-section {
  margin-bottom: 30rpx;
  background: #fff;
  border-radius: 24rpx;
  padding: 30rpx;
  box-shadow: 0 8rpx 24rpx rgba(0, 0, 0, 0.1);
}

.section-header {
  margin-bottom: 20rpx;
}

.section-title {
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
}

.video-box {
  width: 100%;
  height: 500rpx;
  border-radius: 16rpx;
  background: #000;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
}

.result-video, .stream-image {
  width: 100%;
  height: 100%;
}

.placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.placeholder-icon {
  font-size: 100rpx;
  margin-bottom: 20rpx;
  color: rgba(255, 255, 255, 0.6);
}

.placeholder-text {
  font-size: 28rpx;
  color: rgba(255, 255, 255, 0.8);
}

/* 配置区域 */
.config-section {
  background: #fff;
  border-radius: 24rpx;
  padding: 30rpx;
  margin-bottom: 30rpx;
  box-shadow: 0 8rpx 24rpx rgba(0, 0, 0, 0.1);
}

.config-item {
  margin-bottom: 30rpx;
}

.config-item:last-child {
  margin-bottom: 0;
}

.config-label {
  font-size: 30rpx;
  font-weight: bold;
  color: #333;
  display: block;
  margin-bottom: 20rpx;
}

.picker-box {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24rpx;
  border: 2rpx solid #e9ecef;
  border-radius: 16rpx;
  background: #f8f9fa;
}

.picker-text {
  font-size: 28rpx;
  color: #333;
}

.picker-arrow {
  font-size: 24rpx;
  color: #999;
}

.slider-box {
  display: flex;
  align-items: center;
}

slider {
  flex: 1;
  margin-right: 20rpx;
}

.slider-value {
  font-size: 28rpx;
  font-weight: bold;
  color: #007aff;
  min-width: 80rpx;
  text-align: right;
}

/* 控制按钮 */
.control-buttons {
  display: flex;
  justify-content: space-between;
  margin-bottom: 30rpx;
}

.control-btn {
  width: 48%;
  height: 100rpx;
  border-radius: 20rpx;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 8rpx 24rpx rgba(0, 0, 0, 0.15);
  transition: all 0.3s;
}

.start-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.stop-btn {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.control-btn.disabled {
  opacity: 0.5;
  box-shadow: none;
}

.btn-text {
  font-size: 32rpx;
  font-weight: bold;
  color: #fff;
}

/* AI建议区域 */
.suggestion-section {
  background: #fff;
  border-radius: 24rpx;
  padding: 30rpx;
  margin-bottom: 30rpx;
  box-shadow: 0 8rpx 24rpx rgba(0, 0, 0, 0.1);
}

.suggestion-box {
  margin-top: 20rpx;
  padding: 20rpx;
  background: #f8f9fa;
  border-radius: 12rpx;
  min-height: 200rpx;
  line-height: 1.8;
}

/* 进度条 */
.progress-section {
  background: #fff;
  border-radius: 24rpx;
  padding: 30rpx;
  box-shadow: 0 8rpx 24rpx rgba(0, 0, 0, 0.1);
}

.progress-text {
  display: block;
  text-align: center;
  margin-top: 20rpx;
  font-size: 28rpx;
  color: #666;
}
</style>
