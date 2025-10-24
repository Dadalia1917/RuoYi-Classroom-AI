<template>
  <view class="container">
    <!-- 顶部标题 -->
    <view class="header">
      <text class="title">图像检测</text>
    </view>

    <!-- 图片预览区 -->
    <view class="preview-section">
      <view class="image-wrapper" @click="chooseImage">
        <image v-if="imageUrl" :src="imageUrl" mode="aspectFit" class="preview-image"></image>
        <view v-else class="empty-placeholder">
          <text class="icon">📷</text>
          <text class="tip">点击上传图片</text>
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

      <!-- 开始检测按钮 -->
      <button 
        class="detect-btn" 
        :class="{ 'detecting': isPredicting }" 
        @click="predictImage"
        :disabled="isPredicting"
      >
        {{ isPredicting ? '检测中...' : '开始检测' }}
      </button>
    </view>

    <!-- 检测结果 -->
    <view v-if="predictResult" class="result-card">
      <view class="result-title">检测结果</view>
      
      <!-- 原图和结果图 -->
      <view class="result-images" v-if="predictResult.outImg">
        <view class="result-image-item">
          <image :src="originalImage" mode="aspectFit" class="result-img"></image>
          <text class="image-label">原图</text>
        </view>
        <view class="result-image-item">
          <image :src="predictResult.outImg" mode="aspectFit" class="result-img"></image>
          <text class="image-label">检测结果</text>
        </view>
      </view>

      <!-- 检测到的行为标签 -->
      <view class="behavior-tags">
        <view 
          v-for="(label, index) in predictResult.label" 
          :key="index"
          class="behavior-tag"
        >
          <text class="tag-label">{{ formatLabel(label) }}</text>
          <text class="tag-conf">{{ formatConfidencePercent(predictResult.confidence[index]) }}</text>
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
import { addImgRecords } from '@/api/ai/imgRecords'
import { useUserStore } from '@/store/modules/user'
import config from '@/config'

export default {
  data() {
    return {
      imageUrl: '',
      originalImage: '',
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
      predictResult: null
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
  },
  onShow() {
    if (this.modelOptions.length === 0) {
      this.fetchModelList()
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
    
    chooseImage() {
      uni.chooseImage({
        count: 1,
        sizeType: ['compressed'],
        sourceType: ['album', 'camera'],
        success: (res) => {
          this.imageUrl = res.tempFilePaths[0]
          this.originalImage = res.tempFilePaths[0]
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
    
    predictImage() {
      if (!this.imageUrl) {
        uni.showToast({
          title: '请先选择图片',
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
      
      this.isPredicting = true
      
      // 第一步：上传图片到服务器
      uni.uploadFile({
        url: config.baseUrl + '/files/upload',
        filePath: this.imageUrl,
        name: 'file',
        success: (uploadRes) => {
          console.log('文件上传成功:', uploadRes)
          try {
            const uploadData = JSON.parse(uploadRes.data)
            const fileUrl = uploadData.data || uploadData.url
            
            if (!fileUrl) {
              throw new Error('获取文件路径失败')
            }
            
            console.log('文件路径:', fileUrl)
            
            // 第二步：调用检测接口
            const startTime = new Date().toISOString().replace('T', ' ').substring(0, 19)
            uni.request({
              url: config.baseUrl + '/flask/predict',
              method: 'POST',
              data: {
                inputImg: fileUrl,
                weight: this.selectedModel.value,
                conf: this.confidence / 100,
                ai: this.selectedAi.value,
                username: this.username || 'user',
                thinkMode: false,
                startTime: startTime
              },
              header: {
                'Content-Type': 'application/json'
              },
              success: (predictRes) => {
                console.log('检测成功:', predictRes)
                console.log('返回数据类型:', typeof predictRes.data)
                console.log('返回数据内容:', predictRes.data)
                
                try {
                  if (predictRes.data.code === 200) {
                    console.log('data.data 类型:', typeof predictRes.data.data)
                    console.log('data.data 内容:', predictRes.data.data)
                    
                    const resultData = typeof predictRes.data.data === 'string' 
                      ? JSON.parse(predictRes.data.data) 
                      : predictRes.data.data
                    
                    console.log('解析后的 resultData:', resultData)
                    console.log('label 类型:', typeof resultData.label, 'label 值:', resultData.label)
                    console.log('confidence 类型:', typeof resultData.confidence, 'confidence 值:', resultData.confidence)
                    console.log('suggestion:', resultData.suggestion)
                    
                    // 解析 label
                    let labels = resultData.label
                    if (!Array.isArray(labels)) {
                      try {
                        labels = JSON.parse(labels)
                      } catch (e) {
                        console.log('label 不是JSON字符串，作为单值处理')
                        labels = [labels]
                      }
                    }
                    
                    // 解析 confidence
                    let confidences = resultData.confidence
                    if (!Array.isArray(confidences)) {
                      try {
                        confidences = JSON.parse(confidences)
                      } catch (e) {
                        console.log('confidence 不是JSON字符串，作为单值处理')
                        confidences = [confidences]
                      }
                    }
                    
                    console.log('解析后的 labels:', labels)
                    console.log('解析后的 confidences:', confidences)
                    
                    // 确保 confidence 是数字数组
                    // Flask 返回的是带 % 的字符串，如 "95.12%"，需要转换为小数形式（如 0.9512）
                    confidences = confidences.map((c, idx) => {
                      let num
                      if (typeof c === 'string' && c.includes('%')) {
                        // 移除 % 符号并转换为小数
                        num = parseFloat(c.replace('%', '')) / 100
                      } else {
                        num = parseFloat(c)
                      }
                      console.log(`confidence[${idx}]: "${c}" -> ${num}`)
                      return num
                    })
                    
                    this.predictResult = {
                      label: labels,
                      confidence: confidences,
                      allTime: resultData.allTime,
                      suggestion: resultData.suggestion || '',
                      outImg: resultData.outImg,
                      time: startTime
                    }
                    
                    console.log('最终的检测结果:', this.predictResult)
                    console.log('confidence 数组:', this.predictResult.confidence)
                    
                    // 更新显示为检测结果图
                    if (resultData.outImg) {
                      this.imageUrl = resultData.outImg
                    }
                    
                    uni.showToast({
                      title: '检测完成',
                      icon: 'success'
                    })
                  } else {
                    throw new Error(predictRes.data.msg || '检测失败')
                  }
                } catch (err) {
                  console.error('解析检测结果失败:', err)
                  uni.showToast({
                    title: '解析结果失败',
                    icon: 'none'
                  })
                }
              },
              fail: (err) => {
                console.error('检测请求失败:', err)
                uni.showToast({
                  title: '检测失败',
                  icon: 'none'
                })
              },
              complete: () => {
                this.isPredicting = false
              }
            })
          } catch (err) {
            console.error('上传解析失败:', err)
            this.isPredicting = false
            uni.showToast({
              title: '上传失败',
              icon: 'none'
            })
          }
        },
        fail: (err) => {
          console.error('文件上传失败:', err)
          this.isPredicting = false
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
      
      // 将 confidence 数组转换为百分比形式保留2位小数，避免数据库字段过长
      // 例如 0.9453 -> 94.53
      const formattedConfidence = confidences.map(c => 
        parseFloat((c * 100).toFixed(2))
      )
      
      const recordData = {
        username: this.username || 'user',
        label: JSON.stringify(labels),
        confidence: JSON.stringify(formattedConfidence),
        weight: this.selectedModel.value,
        ai: this.selectedAi.value,
        conf: this.confidence / 100,
        startTime: this.predictResult.time || new Date().toISOString(),
        inputImg: this.originalImage || '',
        outImg: this.predictResult.outImg || '',
        allTime: this.predictResult.allTime || '',
        suggestion: this.predictResult.suggestion || ''
      }
      
      console.log('保存数据:', recordData)
      console.log('confidence 长度:', JSON.stringify(formattedConfidence).length)
      
      addImgRecords(recordData).then(response => {
        uni.hideLoading()
        console.log('保存响应:', response)
        uni.showToast({
          title: '保存成功',
          icon: 'success'
        })
        
        setTimeout(() => {
          this.imageUrl = ''
          this.originalImage = ''
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
    },
    
    formatTime(time) {
      if (!time) return ''
      return time.substring(0, 19).replace('T', ' ')
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

.image-wrapper {
  width: 100%;
  height: 400rpx;
  background: #fff;
  border-radius: 20rpx;
  overflow: hidden;
  box-shadow: 0 10rpx 30rpx rgba(0, 0, 0, 0.2);
}

.preview-image {
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

.result-images {
  display: flex;
  justify-content: space-between;
  margin-bottom: 30rpx;
}

.result-image-item {
  width: 48%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.result-img {
  width: 100%;
  height: 250rpx;
  border-radius: 12rpx;
  background: #f5f7fa;
}

.image-label {
  margin-top: 10rpx;
  font-size: 24rpx;
  color: #999;
}

.behavior-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 15rpx;
  margin-bottom: 30rpx;
}

.behavior-tag {
  display: flex;
  align-items: center;
  gap: 10rpx;
  padding: 15rpx 25rpx;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 30rpx;
  color: #fff;
}

.tag-label {
  font-size: 28rpx;
  font-weight: bold;
}

.tag-conf {
  font-size: 24rpx;
  opacity: 0.9;
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
