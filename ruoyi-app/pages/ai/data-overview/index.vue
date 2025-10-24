<template>
  <view class="data-overview-container">
    <!-- 顶部统计卡片 -->
    <view class="stats-cards">
      <view class="stats-card">
        <text class="stats-title">今日检测次数</text>
        <text class="stats-value">{{ todayCount }}</text>
      </view>
      <view class="stats-card">
        <text class="stats-title">本周检测次数</text>
        <text class="stats-value">{{ weekCount }}</text>
      </view>
    </view>
    
    <!-- H5环境下使用ECharts -->
    <!-- #ifdef H5 -->
    <!-- 行为统计饼图 -->
    <view class="chart-section">
      <view class="section-title">学生行为统计（饼图）</view>
      <view id="pieChart" class="chart-container"></view>
    </view>
    
    <!-- 行为统计柱状图 -->
    <view class="chart-section">
      <view class="section-title">学生行为统计（柱状图）</view>
      <view id="barChart" class="chart-container"></view>
    </view>
    <!-- #endif -->
    
    <!-- 非H5环境显示简单统计 -->
    <!-- #ifndef H5 -->
    <view class="chart-section">
      <view class="section-title">学生行为统计</view>
      <view class="behavior-stats">
        <view class="behavior-item" v-for="(item, index) in behaviorStats" :key="index">
          <view class="behavior-color" :style="{ backgroundColor: item.color }"></view>
          <text class="behavior-name">{{ item.name }}</text>
          <text class="behavior-count">{{ item.count }}</text>
        </view>
      </view>
    </view>
    <!-- #endif -->
    
    <!-- 最近检测记录 -->
    <view class="records-section">
      <view class="section-header">
        <text class="section-title">最近检测记录</text>
        <text class="refresh-btn" @click="refreshData">刷新</text>
      </view>
      <view class="records-list">
        <view class="record-item" v-for="(item, index) in recordsList" :key="index">
          <view class="record-info">
            <text class="record-username">{{ item.username }}</text>
            <text class="record-time">{{ item.startTime }}</text>
          </view>
          <view class="record-result">
            <text class="record-label">{{ formatLabel(item.displayLabel || item.label) }}</text>
            <view class="record-type" :class="getTypeClass(item.type)">
              {{ getTypeText(item.type) }}
            </view>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
import { listImgRecords } from '@/api/ai/imgRecords'
import { listCameraRecords } from '@/api/ai/cameraRecords'
import { listVideoRecords } from '@/api/ai/videoRecords'

export default {
  data() {
    return {
      todayCount: 0,
      weekCount: 0,
      behaviorStats: [
        { name: '写字', count: 0, color: '#5470c6' },
        { name: '阅读', count: 0, color: '#91cc75' },
        { name: '听讲', count: 0, color: '#fac858' },
        { name: '睡觉', count: 0, color: '#ee6666' },
        { name: '讨论', count: 0, color: '#73c0de' },
        { name: '举手', count: 0, color: '#3ba272' },
        { name: '低头', count: 0, color: '#fc8452' },
        { name: '玩手机', count: 0, color: '#9a60b4' },
        { name: '站立', count: 0, color: '#ea7ccc' }
      ],
      recordsList: [],
      pieChart: null,
      barChart: null
    }
  },
  onLoad() {
    this.fetchData()
  },
  onUnload() {
    // 销毁图表实例
    if (this.pieChart) {
      this.pieChart.dispose()
      this.pieChart = null
    }
    if (this.barChart) {
      this.barChart.dispose()
      this.barChart = null
    }
  },
  methods: {
    fetchData() {
      Promise.all([
        listImgRecords(),
        listVideoRecords(),
        listCameraRecords()
      ]).then(([imgRes, videoRes, cameraRes]) => {
        const allRecords = [
          ...(imgRes.data || []).map(item => ({ ...item, type: 'img' })),
          ...(videoRes.data || []).map(item => ({ ...item, type: 'video' })),
          ...(cameraRes.data || []).map(item => ({ ...item, type: 'camera' }))
        ]
        
        // 处理统计数据
        this.processStats(allRecords)
        
        // 延迟初始化图表，确保DOM已渲染
        // #ifdef H5
        this.$nextTick(() => {
          setTimeout(() => {
            this.initCharts()
          }, 300)
        })
        // #endif
        
        // 处理记录列表
        this.recordsList = allRecords
          .sort((a, b) => new Date(b.startTime) - new Date(a.startTime))
          .slice(0, 10)
          .map(item => {
            // 解析并格式化 label
            let displayLabel = item.label
            if (typeof item.label === 'string') {
              try {
                // 先尝试解析统计格式 "阅读×15, 写字×8"
                if (item.label.includes('×')) {
                  const firstBehavior = item.label.split(',')[0].split('×')[0]
                  displayLabel = firstBehavior
                } else {
                  // 否则尝试解析JSON数组
                  const parsed = JSON.parse(item.label)
                  if (Array.isArray(parsed) && parsed.length > 0) {
                    displayLabel = parsed[0]
                  }
                }
              } catch (e) {
                console.log('解析 label 失败:', e)
              }
            } else if (Array.isArray(item.label) && item.label.length > 0) {
              displayLabel = item.label[0]
            }
            
            return {
              ...item,
              startTime: this.formatTime(item.startTime),
              displayLabel: displayLabel
            }
          })
      }).catch(error => {
        console.error('获取数据失败:', error)
        uni.showToast({
          title: '获取数据失败',
          icon: 'none'
        })
      })
    },
    
    processStats(records) {
      // 行为统计映射
      const behaviorMap = {
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
      
      const behaviorCount = {}
      records.forEach(record => {
        // 处理label
        let label = record.label
        
        // 如果是统计格式 "阅读×15, 写字×8"，需要展开统计
        if (typeof label === 'string' && label.includes('×')) {
          const behaviors = label.split(',')
          behaviors.forEach(behavior => {
            const match = behavior.trim().match(/(.+)×(\d+)/)
            if (match) {
              const behaviorName = match[1].trim()
              const count = parseInt(match[2])
              behaviorCount[behaviorName] = (behaviorCount[behaviorName] || 0) + count
            }
          })
          return
        }
        
        // 否则按原逻辑处理JSON数组
        if (typeof label === 'string') {
          try {
            label = JSON.parse(label)
          } catch (e) {
            label = [label]
          }
        }
        
        // 如果是数组，统计所有元素
        if (Array.isArray(label)) {
          label.forEach(item => {
            const chineseName = behaviorMap[item] || item
            behaviorCount[chineseName] = (behaviorCount[chineseName] || 0) + 1
          })
        } else {
          // 单个标签
          const chineseName = behaviorMap[label] || label
          behaviorCount[chineseName] = (behaviorCount[chineseName] || 0) + 1
        }
      })
      
      this.behaviorStats.forEach(item => {
        item.count = behaviorCount[item.name] || 0
      })
      
      // 今日和本周统计
      const today = new Date()
      today.setHours(0, 0, 0, 0)
      const weekAgo = new Date(today)
      weekAgo.setDate(weekAgo.getDate() - 7)
      
      this.todayCount = records.filter(record => {
        return new Date(record.startTime) >= today
      }).length
      
      this.weekCount = records.filter(record => {
        return new Date(record.startTime) >= weekAgo
      }).length
    },
    
    // 初始化图表（仅H5）
    initCharts() {
      // #ifdef H5
      if (typeof echarts !== 'undefined') {
        this.initPieChart()
        this.initBarChart()
      } else {
        console.error('ECharts库未加载')
      }
      // #endif
    },
    
    // 初始化饼图
    initPieChart() {
      // #ifdef H5
      const chartDom = document.getElementById('pieChart')
      if (!chartDom) return
      
      if (this.pieChart) {
        this.pieChart.dispose()
      }
      this.pieChart = echarts.init(chartDom)
      
      const chartData = this.behaviorStats
        .filter(item => item.count > 0)
        .map(item => ({
          name: item.name,
          value: item.count,
          itemStyle: { color: item.color }
        }))
      
      const option = {
        tooltip: {
          trigger: 'item',
          formatter: '{b}: {c}次 ({d}%)'
        },
        legend: {
          orient: 'horizontal',
          bottom: 10,
          left: 'center',
          textStyle: {
            fontSize: 12
          }
        },
        series: [
          {
            name: '行为统计',
            type: 'pie',
            radius: ['40%', '70%'],
            center: ['50%', '45%'],
            avoidLabelOverlap: true,
            itemStyle: {
              borderRadius: 10,
              borderColor: '#fff',
              borderWidth: 2
            },
            label: {
              show: true,
              formatter: '{b}\n{c}次',
              fontSize: 11
            },
            emphasis: {
              label: {
                show: true,
                fontSize: 14,
                fontWeight: 'bold'
              }
            },
            labelLine: {
              show: true
            },
            data: chartData.length > 0 ? chartData : [{ name: '暂无数据', value: 1, itemStyle: { color: '#e0e0e0' } }]
          }
        ]
      }
      
      this.pieChart.setOption(option)
      // #endif
    },
    
    // 初始化柱状图
    initBarChart() {
      // #ifdef H5
      const chartDom = document.getElementById('barChart')
      if (!chartDom) return
      
      if (this.barChart) {
        this.barChart.dispose()
      }
      this.barChart = echarts.init(chartDom)
      
      const categories = []
      const data = []
      const colors = []
      
      this.behaviorStats.forEach(item => {
        if (item.count > 0) {
          categories.push(item.name)
          data.push(item.count)
          colors.push(item.color)
        }
      })
      
      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          },
          formatter: '{b}: {c}次'
        },
        grid: {
          left: '10%',
          right: '10%',
          bottom: '10%',
          top: '10%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: categories.length > 0 ? categories : ['暂无数据'],
          axisLabel: {
            fontSize: 11,
            interval: 0,
            rotate: categories.length > 5 ? 45 : 0
          }
        },
        yAxis: {
          type: 'value',
          axisLabel: {
            fontSize: 11
          },
          splitLine: {
            lineStyle: {
              type: 'dashed'
            }
          }
        },
        series: [
          {
            name: '检测次数',
            type: 'bar',
            data: data.length > 0 ? data : [0],
            barWidth: '50%',
            itemStyle: {
              borderRadius: [5, 5, 0, 0],
              color: (params) => {
                return colors[params.dataIndex] || '#5470c6'
              }
            },
            label: {
              show: true,
              position: 'top',
              fontSize: 11
            }
          }
        ]
      }
      
      this.barChart.setOption(option)
      // #endif
    },
    
    formatLabel(label) {
      // 处理统计格式 "阅读×15, 写字×8"
      if (typeof label === 'string' && label.includes('×')) {
        return label.split(',')[0].split('×')[0].trim()
      }
      
      // 处理 JSON 字符串
      let labels = label
      if (typeof label === 'string') {
        try {
          labels = JSON.parse(label)
        } catch (e) {
          labels = [label]
        }
      }
      
      // 如果是数组，取第一个
      if (Array.isArray(labels)) {
        labels = labels[0] || label
      }
      
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
      return labelMap[labels] || labels
    },
    
    getTypeClass(type) {
      const classMap = {
        'img': 'type-img',
        'video': 'type-video',
        'camera': 'type-camera'
      }
      return classMap[type] || 'type-default'
    },
    
    getTypeText(type) {
      const textMap = {
        'img': '图像',
        'video': '视频',
        'camera': '摄像'
      }
      return textMap[type] || type
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
    
    refreshData() {
      uni.showLoading({
        title: '刷新中...'
      })
      this.fetchData()
      setTimeout(() => {
        uni.hideLoading()
        uni.showToast({
          title: '刷新成功',
          icon: 'success'
        })
      }, 1000)
    }
  }
}
</script>

<style>
.data-overview-container {
  padding: 20rpx;
  background-color: #f5f5f5;
  min-height: 100vh;
}

.stats-cards {
  display: flex;
  justify-content: space-between;
  margin-bottom: 30rpx;
}

.stats-card {
  width: 48%;
  background-color: #fff;
  border-radius: 16rpx;
  padding: 30rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
  text-align: center;
}

.stats-title {
  font-size: 28rpx;
  color: #666;
  margin-bottom: 10rpx;
  display: block;
}

.stats-value {
  font-size: 48rpx;
  font-weight: bold;
  color: #333;
  display: block;
}

.chart-section {
  background-color: #fff;
  border-radius: 16rpx;
  padding: 30rpx;
  margin-bottom: 30rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
}

.chart-container {
  width: 100%;
  height: 500rpx;
}

/* 非H5环境显示的简单统计 */
.behavior-stats {
  display: flex;
  flex-wrap: wrap;
}

.behavior-item {
  width: 33.33%;
  display: flex;
  align-items: center;
  margin-bottom: 20rpx;
}

.behavior-color {
  width: 16rpx;
  height: 16rpx;
  border-radius: 4rpx;
  margin-right: 10rpx;
}

.behavior-name {
  font-size: 26rpx;
  color: #666;
  margin-right: 10rpx;
}

.behavior-count {
  font-size: 26rpx;
  font-weight: bold;
  color: #333;
}

.records-section {
  background-color: #fff;
  border-radius: 16rpx;
  padding: 30rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20rpx;
}

.refresh-btn {
  font-size: 28rpx;
  color: #007aff;
}

.records-list {
  max-height: 600rpx;
  overflow-y: auto;
}

.record-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20rpx 0;
  border-bottom: 1rpx solid #f0f0f0;
}

.record-item:last-child {
  border-bottom: none;
}

.record-info {
  display: flex;
  flex-direction: column;
}

.record-username {
  font-size: 30rpx;
  color: #333;
  margin-bottom: 6rpx;
}

.record-time {
  font-size: 24rpx;
  color: #999;
}

.record-result {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.record-label {
  font-size: 28rpx;
  color: #333;
  margin-bottom: 6rpx;
}

.record-type {
  font-size: 24rpx;
  padding: 4rpx 12rpx;
  border-radius: 8rpx;
  color: #fff;
}

.type-img {
  background-color: #007aff;
}

.type-video {
  background-color: #34c759;
}

.type-camera {
  background-color: #ff9500;
}

.type-default {
  background-color: #8e8e93;
}
</style>
