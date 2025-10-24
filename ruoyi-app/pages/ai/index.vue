<template>
  <view class="ai-container">
    <!-- 顶部横幅 -->
    <view class="top-banner">
      <view class="banner-bg">
        <view class="circle circle-1"></view>
        <view class="circle circle-2"></view>
      </view>
      <view class="banner-content">
        <text class="title">AI行为分析</text>
        <text class="subtitle">基于深度学习的课堂行为识别系统</text>
      </view>
    </view>

    <!-- 检测功能区 -->
    <view class="section">
      <view class="section-title">
        <text class="title-icon">🔍</text>
        <text class="title-text">检测功能</text>
      </view>
      
      <view class="card-row">
        <view class="feature-card primary" @click="navigateTo('/pages/ai/img-predict/index')">
          <view class="card-header">
            <text class="card-icon">📷</text>
            <text class="card-badge">快速</text>
          </view>
          <text class="card-title">图像检测</text>
          <text class="card-desc">上传图片进行行为识别</text>
          <view class="card-arrow">→</view>
        </view>
        
        <view class="feature-card success" @click="navigateTo('/pages/ai/video-predict/index')">
          <view class="card-header">
            <text class="card-icon">🎥</text>
            <text class="card-badge">精准</text>
          </view>
          <text class="card-title">视频检测</text>
          <text class="card-desc">上传视频进行行为分析</text>
          <view class="card-arrow">→</view>
        </view>
      </view>
      
      <view class="card-row">
        <view class="feature-card warning" @click="navigateTo('/pages/ai/camera-predict/index')">
          <view class="card-header">
            <text class="card-icon">📸</text>
            <text class="card-badge">实时</text>
          </view>
          <text class="card-title">摄像检测</text>
          <text class="card-desc">实时摄像头行为识别</text>
          <view class="card-arrow">→</view>
        </view>
        
        <view class="feature-card info" @click="navigateTo('/pages/ai/data-overview/index')">
          <view class="card-header">
            <text class="card-icon">📊</text>
            <text class="card-badge">统计</text>
          </view>
          <text class="card-title">数据总览</text>
          <text class="card-desc">查看学生行为统计数据</text>
          <view class="card-arrow">→</view>
        </view>
      </view>
    </view>

    <!-- 历史记录区 -->
    <view class="section">
      <view class="section-title">
        <text class="title-icon">📁</text>
        <text class="title-text">历史记录</text>
      </view>
      
      <view class="record-list">
        <view class="record-card" @click="navigateTo('/pages/ai/img-records/index')">
          <view class="record-icon-wrapper blue">
            <text class="record-icon">📷</text>
          </view>
          <view class="record-info">
            <text class="record-title">图像记录</text>
            <text class="record-desc">查看历史图像检测记录</text>
          </view>
          <view class="record-arrow">›</view>
        </view>
        
        <view class="record-card" @click="navigateTo('/pages/ai/video-records/index')">
          <view class="record-icon-wrapper green">
            <text class="record-icon">🎥</text>
          </view>
          <view class="record-info">
            <text class="record-title">视频记录</text>
            <text class="record-desc">查看历史视频检测记录</text>
          </view>
          <view class="record-arrow">›</view>
        </view>
        
        <view class="record-card" @click="navigateTo('/pages/ai/camera-records/index')">
          <view class="record-icon-wrapper orange">
            <text class="record-icon">📸</text>
          </view>
          <view class="record-info">
            <text class="record-title">摄像记录</text>
            <text class="record-desc">查看历史摄像检测记录</text>
          </view>
          <view class="record-arrow">›</view>
        </view>
      </view>
    </view>

  </view>
</template>

<script>
export default {
  methods: {
    navigateTo(url) {
      uni.navigateTo({
        url: url
      })
    }
  }
}
</script>

<style scoped lang="scss">
.ai-container {
  min-height: 100vh;
  background: linear-gradient(180deg, #f5f7fa 0%, #fff 100%);
  padding-bottom: 40rpx;
}

/* 顶部横幅 */
.top-banner {
  position: relative;
  margin: 30rpx 30rpx 40rpx;
  padding: 50rpx 40rpx;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 24rpx;
  overflow: hidden;
  box-shadow: 0 10rpx 30rpx rgba(102, 126, 234, 0.3);
}

.banner-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.circle {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
}

.circle-1 {
  width: 200rpx;
  height: 200rpx;
  right: -50rpx;
  top: -50rpx;
}

.circle-2 {
  width: 150rpx;
  height: 150rpx;
  right: 100rpx;
  bottom: -30rpx;
}

.banner-content {
  position: relative;
  z-index: 1;
}

.title {
  display: block;
  font-size: 48rpx;
  font-weight: bold;
  color: #fff;
  margin-bottom: 15rpx;
}

.subtitle {
  display: block;
  font-size: 26rpx;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 25rpx;
}

.tech-tags {
  display: flex;
  gap: 15rpx;
}

.tag {
  padding: 8rpx 20rpx;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 20rpx;
  font-size: 22rpx;
  color: #fff;
  backdrop-filter: blur(10rpx);
}

/* 分区 */
.section {
  margin: 0 30rpx 40rpx;
}

.section-title {
  display: flex;
  align-items: center;
  margin-bottom: 25rpx;
}

.title-icon {
  font-size: 36rpx;
  margin-right: 15rpx;
}

.title-text {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
}

/* 功能卡片行 */
.card-row {
  display: flex;
  gap: 20rpx;
  margin-bottom: 20rpx;
}

.feature-card {
  flex: 1;
  position: relative;
  padding: 30rpx 25rpx;
  background: #fff;
  border-radius: 20rpx;
  box-shadow: 0 4rpx 15rpx rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.feature-card.primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.feature-card.success {
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
}

.feature-card.warning {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.feature-card.info {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20rpx;
}

.card-icon {
  font-size: 48rpx;
}

.card-badge {
  padding: 6rpx 15rpx;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 15rpx;
  font-size: 20rpx;
  color: #fff;
}

.card-title {
  display: block;
  font-size: 30rpx;
  font-weight: bold;
  color: #fff;
  margin-bottom: 10rpx;
}

.card-desc {
  display: block;
  font-size: 24rpx;
  color: rgba(255, 255, 255, 0.85);
  margin-bottom: 15rpx;
}

.card-arrow {
  position: absolute;
  right: 25rpx;
  bottom: 25rpx;
  font-size: 32rpx;
  color: rgba(255, 255, 255, 0.6);
  font-weight: bold;
}

/* 记录列表 */
.record-list {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.record-card {
  display: flex;
  align-items: center;
  padding: 30rpx 25rpx;
  background: #fff;
  border-radius: 20rpx;
  box-shadow: 0 4rpx 15rpx rgba(0, 0, 0, 0.06);
}

.record-icon-wrapper {
  width: 80rpx;
  height: 80rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 20rpx;
  margin-right: 25rpx;
}

.record-icon-wrapper.blue {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.record-icon-wrapper.green {
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
}

.record-icon-wrapper.orange {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.record-icon {
  font-size: 40rpx;
}

.record-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.record-title {
  font-size: 30rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 8rpx;
}

.record-desc {
  font-size: 24rpx;
  color: #999;
}

.record-arrow {
  font-size: 40rpx;
  color: #ddd;
}

/* 底部 */
.footer {
  margin: 60rpx 30rpx 0;
  text-align: center;
}

.footer-text {
  font-size: 24rpx;
  color: #999;
}
</style>
