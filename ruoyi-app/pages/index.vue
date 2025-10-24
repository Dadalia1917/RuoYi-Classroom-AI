<template>
  <view class="content">
    <view class="header">
      <view class="logo-icon">🎓</view>
      <view class="text-area">
        <text class="title">课堂行为分析系统</text>
      </view>
    </view>
    
    <view class="quick-actions">
      <view class="section-title">快捷功能</view>
      <view class="action-grid">
        <view class="action-item" @click="navigateTo('/pages/ai/img-predict/index')">
          <view class="action-icon">📷</view>
          <text class="action-text">图像检测</text>
        </view>
        <view class="action-item" @click="navigateTo('/pages/ai/video-predict/index')">
          <view class="action-icon">🎥</view>
          <text class="action-text">视频检测</text>
        </view>
        <view class="action-item" @click="navigateTo('/pages/ai/camera-predict/index')">
          <view class="action-icon">📹</view>
          <text class="action-text">摄像检测</text>
        </view>
        <view class="action-item" @click="navigateTo('/pages/ai/data-overview/index')">
          <view class="action-icon">📊</view>
          <text class="action-text">数据总览</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {}
  },
  methods: {
    navigateTo(url) {
      uni.navigateTo({
        url: url
      })
    }
  }
}
</script>

<style scoped>
  .content {
    display: flex;
    flex-direction: column;
    padding: 20rpx;
    background-color: #f5f5f5;
    min-height: 100vh;
  }
  
  .header {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 40rpx 0;
    background-color: #fff;
    border-radius: 20rpx;
    margin-bottom: 30rpx;
    box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.05);
  }

  .logo-icon {
    font-size: 100rpx;
    margin-bottom: 20rpx;
  }

  .text-area {
    display: flex;
    justify-content: center;
  }

  .title {
    font-size: 36rpx;
    color: #333;
    font-weight: bold;
  }
  
  .quick-actions {
    background-color: #fff;
    border-radius: 20rpx;
    padding: 30rpx;
    margin-bottom: 30rpx;
    box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.05);
  }
  
  .section-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 20rpx;
  }
  
  .action-grid {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
  }
  
  .action-item {
    width: 45%;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 30rpx 0;
    margin-bottom: 20rpx;
    background-color: #f8f8f8;
    border-radius: 16rpx;
    transition: all 0.3s;
  }
  
  .action-item:active {
    transform: scale(0.95);
    background-color: #e6e6e6;
  }
  
  .action-icon {
    font-size: 60rpx;
    margin-bottom: 10rpx;
  }
  
  .action-text {
    font-size: 28rpx;
    color: #333;
  }
</style>
