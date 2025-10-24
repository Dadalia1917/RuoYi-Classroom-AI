<template>
  <view class="camera-records-container">
    <!-- 搜索栏 -->
    <view class="search-section">
      <view class="search-box">
        <input 
          class="search-input" 
          placeholder="搜索用户名" 
          v-model="searchKeyword"
          @confirm="searchRecords"
        />
        <text class="search-btn" @click="searchRecords">搜索</text>
      </view>
    </view>
    
    <!-- 筛选栏 -->
    <view class="filter-section">
      <picker mode="selector" :range="behaviorOptions" range-key="name" @change="onBehaviorChange">
        <view class="filter-item">
          <text class="filter-text">{{ selectedBehavior.name || '全部行为' }}</text>
          <text class="filter-arrow">▼</text>
        </view>
      </picker>
      
      <picker mode="date" @change="onDateChange">
        <view class="filter-item">
          <text class="filter-text">{{ selectedDate || '选择日期' }}</text>
          <text class="filter-arrow">▼</text>
        </view>
      </picker>
    </view>
    
    <!-- 记录列表 -->
    <view class="records-list">
      <view class="record-item" v-for="(item, index) in recordsList" :key="index">
        <view class="record-header">
          <text class="record-username">{{ item.username }}</text>
          <view class="record-type type-camera">摄像</view>
        </view>
        
        <view class="record-content">
          <view class="record-info">
            <view class="info-item">
              <text class="info-label">检测时间:</text>
              <text class="info-value">{{ formatTime(item.startTime) }}</text>
            </view>
            <view class="info-item">
              <text class="info-label">检测模型:</text>
              <text class="info-value">{{ item.weight }}</text>
            </view>
            <view class="info-item">
              <text class="info-label">置信度阈值:</text>
              <text class="info-value">{{ item.conf }}</text>
            </view>
          </view>
        </view>
        
        <view class="record-actions">
          <text class="action-btn view-btn" @click="viewDetail(item)">查看</text>
          <text class="action-btn delete-btn" @click="deleteRecord(item.id)">删除</text>
        </view>
      </view>
      
      <!-- 空状态 -->
      <view v-if="recordsList.length === 0" class="empty-state">
        <text class="empty-icon">📹</text>
        <text class="empty-text">暂无摄像头检测记录</text>
      </view>
    </view>
    
    <!-- 加载更多 -->
    <view v-if="hasMore" class="load-more" @click="loadMore">
      <text class="load-more-text">{{ isLoading ? '加载中...' : '加载更多' }}</text>
    </view>
    
    <!-- 详情弹窗 -->
    <uni-popup ref="detailPopup" type="bottom">
      <view class="detail-popup">
        <view class="detail-header">
          <text class="detail-title">摄像头记录详情</text>
          <text class="close-btn" @click="closeDetail">×</text>
        </view>
        <view class="detail-content">
          <view class="detail-item">
            <text class="detail-label">用户名:</text>
            <text class="detail-value">{{ currentDetail.username }}</text>
          </view>
          <view class="detail-item">
            <text class="detail-label">检测模型:</text>
            <text class="detail-value">{{ currentDetail.weight }}</text>
          </view>
          <view class="detail-item">
            <text class="detail-label">置信度阈值:</text>
            <text class="detail-value">{{ currentDetail.conf }}</text>
          </view>
          <view class="detail-item">
            <text class="detail-label">检测时间:</text>
            <text class="detail-value">{{ formatTime(currentDetail.startTime) }}</text>
          </view>
          
          <!-- 视频播放 -->
          <view v-if="currentDetail.outVideo" class="video-section">
            <text class="detail-label">录制视频:</text>
            <video 
              :src="currentDetail.outVideo" 
              class="detail-video"
              controls
              show-center-play-btn
            ></video>
          </view>
        </view>
      </view>
    </uni-popup>
  </view>
</template>

<script>
import { listCameraRecords, delCameraRecords } from '@/api/ai/cameraRecords'

export default {
  data() {
    return {
      recordsList: [],
      searchKeyword: '',
      selectedBehavior: {},
      selectedDate: '',
      behaviorOptions: [
        { name: '全部行为', value: '' },
        { name: '写作', value: 'Writing' },
        { name: '阅读', value: 'Reading' },
        { name: '听讲', value: 'Listening' },
        { name: '睡觉', value: 'Sleeping' },
        { name: '讨论', value: 'Discussing' },
        { name: '举手', value: 'Raising_hand' },
        { name: '低头', value: 'Bowing' },
        { name: '玩手机', value: 'Phone' },
        { name: '站立', value: 'Stand' }
      ],
      queryParams: {
        pageNum: 1,
        pageSize: 10,
        username: '',
        label: '',
        startTime: ''
      },
      total: 0,
      hasMore: true,
      isLoading: false,
      currentDetail: {}
    }
  },
  onLoad() {
    this.fetchRecords()
  },
  onPullDownRefresh() {
    this.refreshData()
  },
  onReachBottom() {
    if (this.hasMore && !this.isLoading) {
      this.loadMore()
    }
  },
  methods: {
    fetchRecords(isRefresh = false) {
      if (isRefresh) {
        this.queryParams.pageNum = 1
        this.recordsList = []
        this.hasMore = true
      }
      
      if (!this.hasMore) return
      
      this.isLoading = true
      
      listCameraRecords(this.queryParams).then(response => {
        const newRecords = response.data || []
        this.total = response.total || 0
        
        if (isRefresh) {
          this.recordsList = newRecords
        } else {
          this.recordsList = [...this.recordsList, ...newRecords]
        }
        
        // 判断是否还有更多数据
        this.hasMore = this.recordsList.length < this.total
        
        // 更新页码
        if (!isRefresh) {
          this.queryParams.pageNum++
        }
      }).catch(error => {
        console.error('获取记录失败:', error)
        uni.showToast({
          title: '获取记录失败',
          icon: 'none'
        })
      }).finally(() => {
        this.isLoading = false
        if (isRefresh) {
          uni.stopPullDownRefresh()
        }
      })
    },
    
    searchRecords() {
      this.queryParams.username = this.searchKeyword
      this.fetchRecords(true)
    },
    
    onBehaviorChange(e) {
      const index = e.detail.value
      this.selectedBehavior = this.behaviorOptions[index]
      this.queryParams.label = this.selectedBehavior.value
      this.fetchRecords(true)
    },
    
    onDateChange(e) {
      this.selectedDate = e.detail.value
      this.queryParams.startTime = e.detail.value
      this.fetchRecords(true)
    },
    
    loadMore() {
      if (!this.hasMore || this.isLoading) return
      this.queryParams.pageNum++
      this.fetchRecords()
    },
    
    refreshData() {
      this.fetchRecords(true)
    },
    
    deleteRecord(id) {
      uni.showModal({
        title: '确认删除',
        content: '确定要删除这条记录吗？',
        success: (res) => {
          if (res.confirm) {
            uni.showLoading({
              title: '删除中...'
            })
            
            delCameraRecords(id).then(response => {
              uni.hideLoading()
              uni.showToast({
                title: '删除成功',
                icon: 'success'
              })
              this.refreshData()
            }).catch(error => {
              uni.hideLoading()
              console.error('删除失败:', error)
              uni.showToast({
                title: '删除失败',
                icon: 'none'
              })
            })
          }
        }
      })
    },
    
    // 格式化标签摘要（统计显示：写字×7, 阅读×9）
    formatLabelSummary(label) {
      if (!label) return '无'
      
      // 如果已经是格式化后的字符串（包含×），直接返回
      if (typeof label === 'string' && label.includes('×')) {
        return label
      }
      
      // 处理 JSON 字符串
      let labels = label
      if (typeof label === 'string') {
        try {
          labels = JSON.parse(label)
        } catch (e) {
          return label || '无'
        }
      }
      
      if (!Array.isArray(labels)) {
        return label || '无'
      }
      
      // 标签映射
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
      
      // 统计每个标签的出现次数
      const counts = {}
      labels.forEach(l => {
        const translatedLabel = labelMap[l] || l
        counts[translatedLabel] = (counts[translatedLabel] || 0) + 1
      })
      
      // 生成统计摘要
      const summary = Object.entries(counts)
        .sort((a, b) => b[1] - a[1])  // 按出现次数降序
        .map(([label, count]) => `${label}×${count}`)
        .join(', ')
      
      return summary || '无'
    },
    
    // 格式化平均置信度
    formatAverageConfidence(confidence) {
      if (!confidence) return 'N/A'
      
      // 如果已经是百分比字符串（如"85.6%"），直接返回
      if (typeof confidence === 'string' && confidence.includes('%')) {
        return confidence
      }
      
      // 处理 JSON 字符串
      let confs = confidence
      if (typeof confidence === 'string') {
        try {
          confs = JSON.parse(confidence)
        } catch (e) {
          confs = [confidence]
        }
      }
      
      if (!Array.isArray(confs)) {
        confs = [confs]
      }
      
      // 计算平均置信度
      const sum = confs.reduce((acc, c) => {
        // 移除可能的百分号
        const cleanStr = String(c).replace('%', '')
        const num = parseFloat(cleanStr)
        if (isNaN(num)) return acc
        // 如果数字大于1，说明已经是百分比形式
        return acc + (num > 1 ? num : num * 100)
      }, 0)
      
      const avg = sum / confs.length
      return isNaN(avg) ? 'N/A' : avg.toFixed(1) + '%'
    },
    
    // 兼容旧方法（保留给旧代码使用）
    formatLabel(label) {
      return this.formatLabelSummary(label)
    },
    
    formatConfidence(confidence) {
      return this.formatAverageConfidence(confidence)
    },
    
    formatTime(time) {
      if (!time) return ''
      const date = new Date(time)
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      const hours = String(date.getHours()).padStart(2, '0')
      const minutes = String(date.getMinutes()).padStart(2, '0')
      return `${year}-${month}-${day} ${hours}:${minutes}`
    },
    
    viewDetail(item) {
      this.currentDetail = item
      this.$refs.detailPopup.open()
    },
    
    closeDetail() {
      this.$refs.detailPopup.close()
    }
  }
}
</script>

<style>
.camera-records-container {
  padding: 20rpx;
  background-color: #f5f5f5;
  min-height: 100vh;
}

.search-section {
  margin-bottom: 20rpx;
}

.search-box {
  display: flex;
  background-color: #fff;
  border-radius: 12rpx;
  padding: 20rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.1);
}

.search-input {
  flex: 1;
  height: 60rpx;
  font-size: 28rpx;
  padding: 0 20rpx;
  border: 1rpx solid #e9ecef;
  border-radius: 8rpx;
}

.search-btn {
  width: 120rpx;
  height: 60rpx;
  background-color: #007aff;
  color: #fff;
  font-size: 28rpx;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 8rpx;
  margin-left: 20rpx;
}

.filter-section {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20rpx;
}

.filter-item {
  width: 48%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #fff;
  padding: 20rpx;
  border-radius: 12rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.1);
}

.filter-text {
  font-size: 28rpx;
  color: #333;
}

.filter-arrow {
  font-size: 24rpx;
  color: #999;
}

.records-list {
  margin-bottom: 30rpx;
}

.record-item {
  background-color: #fff;
  border-radius: 16rpx;
  padding: 30rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.record-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20rpx;
}

.record-username {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
}

.record-type {
  font-size: 24rpx;
  padding: 6rpx 12rpx;
  border-radius: 8rpx;
  color: #fff;
}

.type-camera {
  background-color: #ff9500;
}

.record-content {
  margin-bottom: 20rpx;
}

.info-item {
  display: flex;
  margin-bottom: 10rpx;
}

.info-label {
  width: 160rpx;
  font-size: 28rpx;
  color: #666;
}

.info-value {
  flex: 1;
  font-size: 28rpx;
  color: #333;
}

.record-actions {
  display: flex;
  justify-content: flex-end;
}

.action-btn {
  font-size: 26rpx;
  padding: 10rpx 20rpx;
  border-radius: 8rpx;
}

.view-btn {
  color: #007aff;
  background-color: rgba(0, 122, 255, 0.1);
  margin-right: 20rpx;
}

.delete-btn {
  color: #ff3b30;
  background-color: rgba(255, 59, 48, 0.1);
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 100rpx 0;
}

.empty-icon {
  font-size: 80rpx;
  margin-bottom: 20rpx;
}

.empty-text {
  font-size: 28rpx;
  color: #999;
}

.load-more {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 80rpx;
  background-color: #fff;
  border-radius: 16rpx;
  margin-bottom: 30rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.load-more-text {
  font-size: 28rpx;
  color: #666;
}

.detail-popup {
  background-color: #fff;
  border-radius: 32rpx 32rpx 0 0;
  max-height: 80vh;
  overflow-y: auto;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 30rpx;
  border-bottom: 1rpx solid #f0f0f0;
}

.detail-title {
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
}

.close-btn {
  font-size: 48rpx;
  color: #999;
  line-height: 1;
}

.detail-content {
  padding: 30rpx;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20rpx;
}

.detail-label {
  font-size: 28rpx;
  color: #666;
  margin-bottom: 10rpx;
}

.detail-value {
  font-size: 28rpx;
  color: #333;
  font-weight: 500;
  text-align: right;
  flex: 1;
  margin-left: 20rpx;
}

.video-section {
  margin-top: 30rpx;
}

.detail-video {
  width: 100%;
  height: 400rpx;
  border-radius: 12rpx;
  margin-top: 10rpx;
}
</style>
