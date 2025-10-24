<template>
  <view class="container">
    <!-- 顶部标题 -->
    <view class="header">
      <text class="title">视频检测</text>
    </view>

    <!-- 视频预览区 -->
    <view class="preview-section">
      <view class="video-wrapper" @click="chooseVideo">
        <video 
          v-if="videoUrl" 
          :src="videoUrl" 
          class="preview-video"
          controls
          objectFit="contain"
        ></video>
        <view v-else class="empty-placeholder">
          <text class="icon">🎥</text>
          <text class="tip">点击上传视频</text>
        </view>
      </view>
    </view>

    <!-- 参数设置卡片 -->
    <view class="param-card">
      <view class="param-title">检测参数</view>
      
      <!-- 模型选择 -->
      <view class="param-item">
        <text class="param-label">检测模型</text>
        <picker mode="selector" :range="modelOptions" range-key="name" @change="onModelChange" class="picker">
          <view class="picker-value">
            <text>{{ selectedModel.name || '请选择模型' }}</text>
            <text class="arrow">▼</text>
          </view>
        </picker>
      </view>

      <!-- 置信度 -->
      <view class="param-item">
        <view class="param-label-row">
          <text class="param-label">置信度</text>
          <text class="param-value-text">{{ (confidence / 100).toFixed(2) }}</text>
        </view>
        <slider 
          :value="confidence" 
          min="0" 
          max="100" 
          @change="onConfidenceChange"
          activeColor="#5C6BC0"
          backgroundColor="#E8EAF6"
          block-size="20"
          block-color="#5C6BC0"
        />
      </view>

      <!-- AI助手 -->
      <view class="param-item">
        <text class="param-label">AI助手</text>
        <picker mode="selector" :range="aiOptions" range-key="name" @change="onAiChange" class="picker">
          <view class="picker-value">
            <text>{{ selectedAi.name || '不使用大模型' }}</text>
            <text class="arrow">▼</text>
          </view>
        </picker>
      </view>

      <!-- 进度条 -->
      <view v-if="isPredicting" class="progress-section">
        <view class="progress-label">
          <text>检测进度</text>
          <text class="progress-value">{{ progress.toFixed(0) }}%</text>
        </view>
        <view class="progress-bar">
          <view class="progress-fill" :style="{ width: progress + '%' }"></view>
        </view>
      </view>

      <!-- 开始检测按钮 -->
      <button 
        class="detect-btn" 
        :class="{ 'detecting': isPredicting }" 
        @click="predictVideo"
        :disabled="isPredicting"
      >
        {{ isPredicting ? '检测中...' : '开始检测' }}
      </button>
    </view>

    <!-- 检测结果 -->
    <view v-if="predictResult" class="result-card">
      <view class="result-title">检测结果</view>
      
      <!-- 行为统计汇总 -->
      <view class="behavior-summary">
        <view class="summary-title">
          <text>行为统计</text>
          <text class="frame-count">共检测 {{ getTotalFrames() }} 帧</text>
        </view>
        
        <view class="summary-tags">
          <view 
            v-for="(item, index) in getBehaviorStatistics()" 
            :key="index"
            class="summary-tag"
          >
            <text class="summary-label">{{ item.label }}</text>
            <text class="summary-count">×{{ item.count }}</text>
            <text class="summary-percent">{{ item.percent }}%</text>
          </view>
        </view>
      </view>

      <!-- 检测结果视频（带检测框的视频） -->
      <view class="result-video-section" v-if="predictResult.outVideo">
        <view class="video-title">检测结果视频</view>
        <video 
          :src="predictResult.outVideo" 
          class="result-video" 
          controls 
          objectFit="contain"
        ></video>
      </view>

      <!-- 统计信息 -->
      <view class="stats-section">
        <view class="stat-item">
          <text class="stat-label">检测时长</text>
          <text class="stat-value">{{ predictResult.allTime }}</text>
        </view>
        <view class="stat-item">
          <text class="stat-label">平均置信度</text>
          <text class="stat-value">{{ getAverageConfidence() }}%</text>
        </view>
      </view>

      <!-- AI建议 -->
      <view class="ai-suggestion">
        <view class="suggestion-title">
          <text class="icon">🤖</text>
          <text>AI教学建议</text>
        </view>
        <view class="suggestion-content">
          <text v-if="predictResult.suggestion && predictResult.suggestion.trim()">{{ predictResult.suggestion }}</text>
          <text v-else class="no-suggestion">未启用AI助手</text>
        </view>
      </view>

      <!-- 保存按钮 -->
      <button class="save-btn" @click="saveResult">保存到记录</button>
    </view>
  </view>
</template>

<script>
import { getModelList } from '@/api/ai/predict'
import { addVideoRecords } from '@/api/ai/videoRecords'
import { useUserStore } from '@/store/modules/user'
import config from '@/config'

export default {
  data() {
    return {
      videoUrl: '',
      originalVideo: '',
      modelOptions: [],
      selectedModel: {},
      aiOptions: [
        { name: '不使用大模型', value: '不使用AI' },
        { name: 'Deepseek-R1', value: 'Deepseek-R1' },
        { name: 'Qwen', value: 'Qwen' },
        { name: 'Deepseek-R1（局域网）', value: 'Deepseek-R1-LAN' },
        { name: 'Qwen3.0（局域网）', value: 'Qwen3.0-LAN' },
        { name: 'Qwen2.5-VL（局域网）', value: 'Qwen2.5-VL-LAN' },
        { name: 'Qwen2.5-Omni（局域网）', value: 'Qwen2.5-Omni-LAN' },
        { name: 'Gemma3（局域网）', value: 'Gemma3-LAN' },
        { name: 'Deepseek-R1（本地）', value: 'Deepseek-R1-Local' },
        { name: 'Qwen3.0（本地）', value: 'Qwen3.0-Local' },
        { name: 'Qwen2.5-VL（本地）', value: 'Qwen2.5-VL-Local' },
        { name: 'Qwen2.5-Omni（本地）', value: 'Qwen2.5-Omni-Local' },
        { name: 'Gemma3（本地）', value: 'Gemma3-Local' }
      ],
      selectedAi: { name: '不使用大模型', value: '不使用AI' },
      confidence: 50,
      isPredicting: false,
      progress: 0,
      predictResult: null,
      socket: null,  // Socket.IO连接
      socketConnected: false,  // Socket连接状态
      progressTimer: null,  // 进度模拟定时器
      lastSocketProgress: 0  // 上次Socket推送的进度
    }
  },
  computed: {
    userId() {
      const userStore = useUserStore()
      return userStore.id
    },
    username() {
      const userStore = useUserStore()
      return userStore.name
    }
  },
  onLoad() {
    this.fetchModelList()
    this.initSocket()
  },
  onShow() {
    if (this.modelOptions.length === 0) {
      this.fetchModelList()
    }
  },
  onUnload() {
    this.disconnectSocket()
    // 清理进度定时器
    if (this.progressTimer) {
      clearInterval(this.progressTimer)
      this.progressTimer = null
    }
  },
  methods: {
    fetchModelList() {
      const defaultModels = [
        { name: 'RT-DETR.pt', value: 'RT-DETR.pt' },
        { name: 'best.pt', value: 'best.pt' },
        { name: 'yolov8n.pt', value: 'yolov8n.pt' }
      ]
      
      getModelList().then(response => {
        try {
          let data = response.data
          if (typeof data === 'string') {
            data = JSON.parse(data)
          }
          
          const weightItems = data.weight_items || data
          if (Array.isArray(weightItems) && weightItems.length > 0) {
            this.modelOptions = weightItems.map(item => ({
              name: item.label || item.value || item,
              value: item.value || item.label || item
            }))
            this.selectedModel = this.modelOptions[0]
          } else {
            this.modelOptions = defaultModels
            this.selectedModel = this.modelOptions[0]
          }
        } catch (error) {
          console.error('解析模型列表失败:', error)
          this.modelOptions = defaultModels
          this.selectedModel = this.modelOptions[0]
        }
      }).catch(error => {
        console.error('获取模型列表失败:', error)
        this.modelOptions = defaultModels
        this.selectedModel = this.modelOptions[0]
      })
    },
    
    chooseVideo() {
      uni.chooseVideo({
        count: 1,
        sourceType: ['album', 'camera'],
        maxDuration: 60,
        camera: 'back',
        success: (res) => {
          this.videoUrl = res.tempFilePath
          this.originalVideo = res.tempFilePath
          this.predictResult = null
        }
      })
    },
    
    onModelChange(e) {
      const index = e.detail.value
      this.selectedModel = this.modelOptions[index]
    },
    
    onAiChange(e) {
      const index = e.detail.value
      this.selectedAi = this.aiOptions[index]
    },
    
    onConfidenceChange(e) {
      this.confidence = e.detail.value
    },
    
    // 初始化Socket.IO连接
    initSocket() {
      // #ifdef H5
      if (typeof io !== 'undefined') {
        try {
          this.socket = io('http://127.0.0.1:5000', {
            transports: ['polling', 'websocket'],
            reconnection: true,
            reconnectionAttempts: 5,
            reconnectionDelay: 1000
          })
          
          this.socket.on('connect', () => {
            console.log('✅ Socket.IO连接成功')
            this.socketConnected = true
          })
          
          this.socket.on('connect_error', (err) => {
            console.error('❌ Socket.IO连接失败:', err)
            this.socketConnected = false
          })
          
          this.socket.on('disconnect', (reason) => {
            console.log('Socket.IO断开:', reason)
            this.socketConnected = false
          })
          
          // 监听进度更新
          this.socket.on('progress', (data) => {
            const progressValue = typeof data === 'object' && data.data 
              ? parseInt(data.data) 
              : parseInt(data)
            console.log('📊 Socket.IO进度更新:', progressValue + '%')
            
            // 使用真实进度，停止模拟进度
            if (progressValue > this.lastSocketProgress) {
              this.lastSocketProgress = progressValue
              this.progress = progressValue
              
              // 如果收到了真实进度，停止模拟
              if (this.progressTimer && progressValue > 10) {
                clearInterval(this.progressTimer)
                this.progressTimer = null
                console.log('🛑 检测到Socket进度推送，停止模拟进度')
              }
            }
          })
          
          // 监听AI建议
          this.socket.on('suggestion', (data) => {
            console.log('收到AI建议')
            if (this.predictResult) {
              this.predictResult.suggestion = data
            }
          })
          
          // 监听视频处理完成
          this.socket.on('video_complete', (data) => {
            console.log('=== 视频处理完成 ===')
            console.log('Socket.IO推送的完整数据:', data)
            
            // Flask推送的数据可能是字符串或对象
            let resultData = data
            if (typeof data === 'string') {
              try {
                resultData = JSON.parse(data)
              } catch (e) {
                console.error('解析Socket.IO数据失败:', e)
                resultData = { url: data }
              }
            }
            
            console.log('解析后的结果数据:', resultData)
            
            if (this.predictResult) {
              // 更新输出视频URL
              if (resultData.url || resultData.outVideo) {
                this.predictResult.outVideo = resultData.url || resultData.outVideo
                this.videoUrl = this.predictResult.outVideo  // 同时更新显示的视频URL
                console.log('✅ 已更新视频URL:', this.predictResult.outVideo)
              }
              
              // 更新检测结果（label和confidence）
              if (resultData.label) {
                this.predictResult.label = Array.isArray(resultData.label) ? resultData.label : [resultData.label]
                console.log('✅ 已更新label:', this.predictResult.label)
              }
              
              if (resultData.confidence) {
                this.predictResult.confidence = Array.isArray(resultData.confidence) ? resultData.confidence : [resultData.confidence]
                console.log('✅ 已更新confidence:', this.predictResult.confidence)
              }
              
              // 更新检测时长
              if (resultData.allTime || resultData.all_time) {
                this.predictResult.allTime = resultData.allTime || resultData.all_time
                console.log('✅ 已更新检测时长:', this.predictResult.allTime)
              }
              
              // 更新AI建议（如果有）
              if (resultData.suggestion) {
                this.predictResult.suggestion = resultData.suggestion
                console.log('✅ 已更新AI建议')
              }
              
              // 标记检测完成
              this.isPredicting = false
              this.progress = 100
              
              // 清理进度模拟定时器
              if (this.progressTimer) {
                clearInterval(this.progressTimer)
                this.progressTimer = null
              }
              
              console.log('=== 最终的predictResult ===', this.predictResult)
              
              uni.showToast({
                title: '视频检测完成！',
                icon: 'success',
                duration: 2000
              })
            }
          })
        } catch (error) {
          console.error('Socket.IO初始化失败:', error)
        }
      } else {
        console.warn('Socket.IO库未加载')
      }
      // #endif
    },
    
    // 断开Socket.IO连接
    disconnectSocket() {
      if (this.socket) {
        this.socket.disconnect()
        this.socket = null
        this.socketConnected = false
      }
    },
    
    // 模拟进度更新（参考摄像头检测）
    simulateProgress() {
      // 清除之前的定时器
      if (this.progressTimer) {
        clearInterval(this.progressTimer)
        this.progressTimer = null
      }
      
      // 初始进度
      this.progress = 5
      
      // 启动模拟进度
      this.progressTimer = setInterval(() => {
        // 如果已经收到Socket.IO的真实进度，不再模拟
        if (this.lastSocketProgress > 10) {
          console.log('🛑 已有真实进度，停止模拟')
          clearInterval(this.progressTimer)
          this.progressTimer = null
          return
        }
        
        // 模拟进度增长，最多到85%（留15%给真实完成）
        if (this.progress < 85) {
          this.progress += Math.random() * 3 + 1  // 每次增加1-4%
          if (this.progress > 85) {
            this.progress = 85
          }
          console.log('🔄 模拟进度:', this.progress.toFixed(0) + '%')
        }
      }, 800)  // 每800ms更新一次
    },
    
    predictVideo() {
      if (!this.videoUrl) {
        uni.showToast({
          title: '请先选择视频',
          icon: 'none'
        })
        return
      }
      
      if (!this.selectedModel.value) {
        uni.showToast({
          title: '请选择模型',
          icon: 'none'
        })
        return
      }
      
      // #ifndef H5
      uni.showModal({
        title: '功能说明',
        content: '由于技术限制，视频检测功能需要实时流式处理和Socket.IO支持，暂不支持移动端。\n\n建议访问PC端网页版（http://localhost:8080）使用完整的视频检测功能。\n\n移动端推荐使用【图片检测】或【摄像头检测】功能。',
        showCancel: false,
        confirmText: '我知道了'
      })
      return
      // #endif
      
      this.isPredicting = true
      this.progress = 0
      this.lastSocketProgress = 0
      
      // 开始模拟进度（如果Socket.IO没有推送真实进度，这个模拟会提供视觉反馈）
      this.simulateProgress()
      
      // 第一步：上传视频到服务器
      uni.uploadFile({
        url: config.baseUrl + '/files/upload',
        filePath: this.videoUrl,
        name: 'file',
        success: (uploadRes) => {
          console.log('视频上传成功:', uploadRes)
          try {
            const uploadData = JSON.parse(uploadRes.data)
            const fileUrl = uploadData.data || uploadData.url
            
            if (!fileUrl) {
              throw new Error('获取文件路径失败')
            }
            
            console.log('视频路径:', fileUrl)
            this.originalVideo = fileUrl
            
            // 第二步：直接调用Flask的视频检测接口（已启用CORS）
            const startTime = new Date().toISOString().replace('T', ' ').substring(0, 19)
            
            console.log('开始视频检测，文件URL:', fileUrl)
            
            // 初始化预测结果容器（Socket.IO会填充数据）
            this.predictResult = {
              label: [],
              confidence: [],
              weight: this.selectedModel.value,
              outVideo: '',
              ai: this.selectedAi.name,
              suggestion: '',
              startTime: startTime,
              endTime: '',
              allTime: '0秒',
              username: this.username || 'user'
            }
            
            // 直接调用Flask接口（Flask已启用CORS，无跨域问题）
            const flaskUrl = `http://127.0.0.1:5000/predictVideo?username=${this.username || 'user'}&weight=${this.selectedModel.value}&conf=${this.confidence / 100}&startTime=${encodeURIComponent(startTime)}&ai=${encodeURIComponent(this.selectedAi.value)}&thinkMode=false&inputVideo=${encodeURIComponent(fileUrl)}`
            
            console.log('直接调用Flask视频检测:', flaskUrl)
            
            // 发送GET请求触发Flask处理（不等待响应，通过Socket.IO接收结果）
            uni.request({
              url: flaskUrl,
              method: 'GET',
              success: (res) => {
                console.log('Flask响应:', res)
                // 视频检测已开始，等待Socket.IO推送结果
                // 注释掉弹窗，使用进度条显示状态即可
                // uni.showToast({
                //   title: '视频检测已开始，请等待...',
                //   icon: 'loading',
                //   duration: 3000
                // })
              },
              fail: (err) => {
                console.error('调用Flask失败:', err)
                this.isPredicting = false
                // 清理进度模拟定时器
                if (this.progressTimer) {
                  clearInterval(this.progressTimer)
                  this.progressTimer = null
                }
                uni.showToast({
                  title: 'Flask连接失败',
                  icon: 'none'
                })
              }
            })
            
          } catch (error) {
            console.error('处理上传响应失败:', error)
            this.isPredicting = false
            // 清理进度模拟定时器
            if (this.progressTimer) {
              clearInterval(this.progressTimer)
              this.progressTimer = null
            }
            uni.showToast({
              title: '上传失败',
              icon: 'none'
            })
          }
        },
        fail: (err) => {
          console.error('视频上传失败:', err)
          this.isPredicting = false
          // 清理进度模拟定时器
          if (this.progressTimer) {
            clearInterval(this.progressTimer)
            this.progressTimer = null
          }
          uni.showToast({
            title: '上传失败',
            icon: 'none'
          })
        }
      })
    },
    
    saveResult() {
      if (!this.predictResult) {
        uni.showToast({
          title: '没有可保存的结果',
          icon: 'none'
        })
        return
      }
      
      uni.showLoading({
        title: '保存中...'
      })
      
      // 确保 label 和 confidence 是数组
      let labels = this.predictResult.label
      let confidences = this.predictResult.confidence
      
      if (!Array.isArray(labels)) {
        labels = [labels]
      }
      if (!Array.isArray(confidences)) {
        confidences = [confidences]
      }
      
      // 🔥 统计各种行为的出现次数（类似图像检测的显示方式）
      // 例如：阅读*15, 写字*8, 听讲*3
      const labelCount = {}
      labels.forEach(label => {
        labelCount[label] = (labelCount[label] || 0) + 1
      })
      
      // 生成汇总字符串
      const labelSummary = Object.entries(labelCount)
        .sort((a, b) => b[1] - a[1]) // 按出现次数降序排序
        .map(([label, count]) => `${this.formatLabel(label)}×${count}`)
        .join(', ')
      
      // 计算平均置信度
      const totalFrames = labels.length
      const avgConfidence = (confidences.reduce((a, b) => a + b, 0) / confidences.length * 100).toFixed(2)
      
      const recordData = {
        username: this.username || 'user',
        label: `${labelSummary} (共${totalFrames}帧)`,
        confidence: `${avgConfidence}%`,
        weight: this.selectedModel.value,
        ai: this.selectedAi.value,
        conf: this.confidence / 100,
        startTime: this.predictResult.startTime || new Date().toISOString().replace('T', ' ').substring(0, 19),
        inputVideo: this.originalVideo || '',
        outVideo: this.predictResult.outVideo || '',
        allTime: this.predictResult.allTime || '',
        suggestion: this.predictResult.suggestion || ''
      }
      
      console.log('保存数据:', recordData)
      console.log('行为统计:', labelCount)
      console.log('label 长度:', recordData.label.length)
      console.log('confidence:', recordData.confidence)
      
      addVideoRecords(recordData).then(response => {
        uni.hideLoading()
        console.log('保存响应:', response)
        uni.showToast({
          title: '保存成功',
          icon: 'success'
        })
        
        setTimeout(() => {
          this.videoUrl = ''
          this.originalVideo = ''
          this.predictResult = null
        }, 1500)
      }).catch(error => {
        uni.hideLoading()
        console.error('保存失败:', error)
        uni.showToast({
          title: '保存失败: ' + (error.msg || error.message || '未知错误'),
          icon: 'none',
          duration: 3000
        })
      })
    },
    
    // 获取最后一帧的标签
    getLastLabel() {
      if (!this.predictResult || !this.predictResult.label) {
        return ''
      }
      const labels = Array.isArray(this.predictResult.label) 
        ? this.predictResult.label 
        : [this.predictResult.label]
      return labels[labels.length - 1] || ''
    },
    
    // 获取最后一帧的置信度
    getLastConfidence() {
      if (!this.predictResult || !this.predictResult.confidence) {
        return 0
      }
      const confidences = Array.isArray(this.predictResult.confidence) 
        ? this.predictResult.confidence 
        : [this.predictResult.confidence]
      return confidences[confidences.length - 1] || 0
    },
    
    // 获取总帧数
    getTotalFrames() {
      if (!this.predictResult || !this.predictResult.label) {
        return 0
      }
      const labels = Array.isArray(this.predictResult.label) 
        ? this.predictResult.label 
        : [this.predictResult.label]
      return labels.length
    },
    
    // 获取平均置信度
    getAverageConfidence() {
      if (!this.predictResult || !this.predictResult.confidence) {
        return '0.0'
      }
      const confidences = Array.isArray(this.predictResult.confidence) 
        ? this.predictResult.confidence 
        : [this.predictResult.confidence]
      
      if (confidences.length === 0) {
        return '0.0'
      }
      
      const sum = confidences.reduce((acc, val) => acc + parseFloat(val), 0)
      const avg = sum / confidences.length
      return (avg * 100).toFixed(1)
    },
    
    // 获取行为统计数据
    getBehaviorStatistics() {
      if (!this.predictResult || !this.predictResult.label) {
        return []
      }
      const labels = Array.isArray(this.predictResult.label) 
        ? this.predictResult.label 
        : [this.predictResult.label]
      
      if (labels.length === 0) {
        return []
      }
      
      // 统计每种行为的出现次数
      const labelCount = {}
      labels.forEach(label => {
        labelCount[label] = (labelCount[label] || 0) + 1
      })
      
      // 转换为数组并计算百分比
      const total = labels.length
      return Object.entries(labelCount)
        .map(([label, count]) => ({
          label: this.formatLabel(label),
          count: count,
          percent: ((count / total) * 100).toFixed(1)
        }))
        .sort((a, b) => b.count - a.count) // 按出现次数降序排序
    },
    
    formatLabel(label) {
      const labelMap = {
        'Writing': '写字',
        'Reading': '阅读',
        'Listening': '听讲',
        'Sleeping': '睡觉',
        'Discussing': '讨论',
        'Raising_hand': '举手',
        'Bowing': '低头',
        'Phone': '玩手机',
        'Stand': '站立'
      }
      return labelMap[label] || label
    },
    
    formatConfidencePercent(confidence) {
      // 确保 confidence 是数字
      const conf = parseFloat(confidence)
      if (isNaN(conf)) {
        return 'N/A'
      }
      return (conf * 100).toFixed(1) + '%'
    }
  }
}
</script>

<style scoped>
.container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20rpx;
}

.header {
  text-align: center;
  padding: 40rpx 0 20rpx;
}

.title {
  font-size: 48rpx;
  font-weight: bold;
  color: #fff;
  text-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.2);
}

/* 预览区 */
.preview-section {
  margin: 20rpx 0;
}

.video-wrapper {
  width: 100%;
  height: 400rpx;
  background: #fff;
  border-radius: 20rpx;
  overflow: hidden;
  box-shadow: 0 10rpx 30rpx rgba(0, 0, 0, 0.2);
}

.preview-video {
  width: 100%;
  height: 100%;
}

.empty-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.icon {
  font-size: 80rpx;
  margin-bottom: 20rpx;
}

.tip {
  font-size: 28rpx;
  color: #666;
}

/* 参数卡片 */
.param-card {
  background: #fff;
  border-radius: 20rpx;
  padding: 30rpx;
  margin: 20rpx 0;
  box-shadow: 0 10rpx 30rpx rgba(0, 0, 0, 0.2);
}

.param-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 30rpx;
}

.param-item {
  margin-bottom: 30rpx;
}

.param-label {
  font-size: 28rpx;
  color: #666;
  margin-bottom: 15rpx;
  display: block;
}

.param-label-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15rpx;
}

.param-value-text {
  font-size: 28rpx;
  color: #5C6BC0;
  font-weight: bold;
}

.picker {
  width: 100%;
}

.picker-value {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20rpx;
  background: #f5f7fa;
  border-radius: 12rpx;
  font-size: 28rpx;
}

.arrow {
  color: #999;
  font-size: 24rpx;
}

.progress-section {
  margin-bottom: 30rpx;
}

.progress-label {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15rpx;
  font-size: 28rpx;
  color: #666;
}

.progress-value {
  color: #5C6BC0;
  font-weight: bold;
}

.progress-bar {
  width: 100%;
  height: 20rpx;
  background: #E8EAF6;
  border-radius: 10rpx;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  border-radius: 10rpx;
  transition: width 0.3s ease;
}

.detect-btn {
  width: 100%;
  height: 90rpx;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  border: none;
  border-radius: 45rpx;
  font-size: 32rpx;
  font-weight: bold;
  margin-top: 20rpx;
  box-shadow: 0 8rpx 20rpx rgba(102, 126, 234, 0.4);
}

.detect-btn.detecting {
  opacity: 0.7;
}

/* 结果卡片 */
.result-card {
  background: #fff;
  border-radius: 20rpx;
  padding: 30rpx;
  margin: 20rpx 0;
  box-shadow: 0 10rpx 30rpx rgba(0, 0, 0, 0.2);
}

.result-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 30rpx;
}

/* 检测结果视频 */
.result-video-section {
  margin-bottom: 30rpx;
  padding: 25rpx;
  background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
  border-radius: 16rpx;
}

.video-title {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
}

.result-video {
  width: 100%;
  height: 400rpx;
  border-radius: 16rpx;
  background: #000;
}

/* 行为统计汇总 */
.behavior-summary {
  margin-bottom: 30rpx;
  padding: 25rpx;
  background: linear-gradient(135deg, #fff8e1 0%, #ffe0b2 100%);
  border-radius: 16rpx;
}

.summary-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20rpx;
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
}

.summary-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 15rpx;
}

.summary-tag {
  display: flex;
  align-items: center;
  gap: 8rpx;
  padding: 12rpx 20rpx;
  background: #fff;
  border-radius: 25rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.1);
}

.summary-label {
  font-size: 26rpx;
  font-weight: bold;
  color: #333;
}

.summary-count {
  font-size: 24rpx;
  color: #667eea;
  font-weight: bold;
}

.summary-percent {
  font-size: 22rpx;
  color: #999;
}

/* 最后一帧检测结果 */
.last-frame-result {
  margin-bottom: 30rpx;
  padding: 25rpx;
  background: linear-gradient(135deg, #f5f7fa 0%, #e3f2fd 100%);
  border-radius: 16rpx;
}

.frame-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20rpx;
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
}

.frame-count {
  font-size: 24rpx;
  color: #666;
  font-weight: normal;
}

.frame-detection {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.detection-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20rpx;
  background: #fff;
  border-radius: 12rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.05);
}

.detection-label {
  font-size: 26rpx;
  color: #666;
}

.detection-value {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
}

.confidence-value {
  color: #667eea;
}

.stats-section {
  display: flex;
  justify-content: space-around;
  margin-bottom: 30rpx;
  padding: 20rpx;
  background: #f5f7fa;
  border-radius: 12rpx;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10rpx;
}

.stat-label {
  font-size: 24rpx;
  color: #999;
}

.stat-value {
  font-size: 32rpx;
  font-weight: bold;
  color: #5C6BC0;
}

.ai-suggestion {
  margin-bottom: 30rpx;
  padding: 25rpx;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  border-radius: 15rpx;
}

.suggestion-title {
  display: flex;
  align-items: center;
  gap: 10rpx;
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 15rpx;
}

.suggestion-content {
  font-size: 26rpx;
  color: #666;
  line-height: 1.8;
}

.no-suggestion {
  color: #999;
  font-style: italic;
}

.save-btn {
  width: 100%;
  height: 80rpx;
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
  color: #fff;
  border: none;
  border-radius: 40rpx;
  font-size: 30rpx;
  font-weight: bold;
  box-shadow: 0 8rpx 20rpx rgba(17, 153, 142, 0.4);
}
</style>
