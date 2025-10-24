<template>
  <view class="work-container">
    <!-- 顶部欢迎横幅 -->
    <view class="welcome-banner">
      <view class="banner-content">
        <text class="welcome-title">课堂行为检测</text>
        <text class="welcome-subtitle">AI智能行为分析系统</text>
        <text class="welcome-desc">基于深度学习的课堂行为识别</text>
      </view>
      <view class="banner-decoration">
        <view class="circle circle-1"></view>
        <view class="circle circle-2"></view>
        <view class="circle circle-3"></view>
      </view>
    </view>

    <!-- AI功能模块 -->
    <view class="section">
      <view class="section-header">
        <view class="section-title-wrapper">
          <text class="section-icon">🤖</text>
          <text class="section-title">AI行为分析</text>
        </view>
      </view>
      
      <view class="function-grid">
        <view class="function-card" @click="navigateTo('/pages/ai/img-predict/index')">
          <view class="card-icon-wrapper blue">
            <text class="card-emoji">📷</text>
          </view>
          <text class="card-title">图像检测</text>
        </view>
        
        <view class="function-card" @click="navigateTo('/pages/ai/video-predict/index')">
          <view class="card-icon-wrapper green">
            <text class="card-emoji">🎥</text>
          </view>
          <text class="card-title">视频检测</text>
        </view>
        
        <view class="function-card" @click="navigateTo('/pages/ai/camera-predict/index')">
          <view class="card-icon-wrapper orange">
            <text class="card-emoji">📸</text>
          </view>
          <text class="card-title">摄像检测</text>
        </view>
        
        <view class="function-card" @click="navigateTo('/pages/ai/data-overview/index')">
          <view class="card-icon-wrapper purple">
            <text class="card-emoji">📊</text>
          </view>
          <text class="card-title">数据总览</text>
        </view>
        
        <view class="function-card" @click="navigateTo('/pages/ai/img-records/index')">
          <view class="card-icon-wrapper red">
            <text class="card-emoji">📁</text>
          </view>
          <text class="card-title">图像记录</text>
        </view>
        
        <view class="function-card" @click="navigateTo('/pages/ai/video-records/index')">
          <view class="card-icon-wrapper teal">
            <text class="card-emoji">📂</text>
          </view>
          <text class="card-title">视频记录</text>
        </view>
        
        <view class="function-card" @click="navigateTo('/pages/ai/camera-records/index')">
          <view class="card-icon-wrapper indigo">
            <text class="card-emoji">📹</text>
          </view>
          <text class="card-title">摄像记录</text>
        </view>
      </view>
    </view>

    <!-- 系统管理模块 -->
    <view class="section">
      <view class="section-header">
        <view class="section-title-wrapper">
          <text class="section-icon">⚙️</text>
          <text class="section-title">系统管理</text>
        </view>
      </view>
      
      <view class="function-grid">
        <view class="function-card" @click="openSystemPage('user')">
          <view class="card-icon-wrapper gray">
            <text class="card-emoji">👤</text>
          </view>
          <text class="card-title">用户管理</text>
        </view>
        
        <view class="function-card" @click="openSystemPage('role')">
          <view class="card-icon-wrapper gray">
            <text class="card-emoji">👥</text>
          </view>
          <text class="card-title">角色管理</text>
        </view>
        
        <view class="function-card" @click="openSystemPage('menu')">
          <view class="card-icon-wrapper gray">
            <text class="card-emoji">📋</text>
          </view>
          <text class="card-title">菜单管理</text>
        </view>
        
        <view class="function-card" @click="openSystemPage('dept')">
          <view class="card-icon-wrapper gray">
            <text class="card-emoji">🏢</text>
          </view>
          <text class="card-title">部门管理</text>
        </view>
        
        <view class="function-card" @click="openSystemPage('post')">
          <view class="card-icon-wrapper gray">
            <text class="card-emoji">💼</text>
          </view>
          <text class="card-title">岗位管理</text>
        </view>
        
        <view class="function-card" @click="openSystemPage('dict')">
          <view class="card-icon-wrapper gray">
            <text class="card-emoji">📖</text>
          </view>
          <text class="card-title">字典管理</text>
        </view>
        
        <view class="function-card" @click="openSystemPage('config')">
          <view class="card-icon-wrapper gray">
            <text class="card-emoji">⚙️</text>
          </view>
          <text class="card-title">参数设置</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
function navigateTo(url) {
  uni.navigateTo({
    url: url
  })
}

function showToast() {
  uni.showToast({
    title: '模块建设中~',
    icon: 'none'
  })
}

// 打开系统管理页面
function openSystemPage(type) {
  // #ifdef H5
  // H5环境下，通过webview跳转到PC端管理页面
  const pageMap = {
    'user': 'system/user',
    'role': 'system/role',
    'menu': 'system/menu',
    'dept': 'system/dept',
    'post': 'system/post',
    'dict': 'system/dict/type',
    'config': 'system/config'
  }
  
  const pagePath = pageMap[type]
  if (pagePath) {
    const pcUrl = `http://localhost:8081/${pagePath}`
    uni.navigateTo({
      url: `/pages/common/webview/index?url=${encodeURIComponent(pcUrl)}&title=${getPageTitle(type)}`
    })
  }
  // #endif
  
  // #ifndef H5
  // 非H5环境下提示需在PC端使用
  uni.showModal({
    title: '提示',
    content: '系统管理功能建议在PC端使用，体验更佳',
    confirmText: '知道了',
    showCancel: false
  })
  // #endif
}

function getPageTitle(type) {
  const titleMap = {
    'user': '用户管理',
    'role': '角色管理',
    'menu': '菜单管理',
    'dept': '部门管理',
    'post': '岗位管理',
    'dict': '字典管理',
    'config': '参数设置'
  }
  return titleMap[type] || '系统管理'
}
</script>

<style scoped lang="scss">
.work-container {
  min-height: 100vh;
  background: linear-gradient(180deg, #f5f7fa 0%, #fff 100%);
  padding-bottom: 40rpx;
}

/* 欢迎横幅 */
.welcome-banner {
  position: relative;
  margin: 30rpx 30rpx 40rpx;
  padding: 50rpx 40rpx;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 24rpx;
  overflow: hidden;
  box-shadow: 0 10rpx 30rpx rgba(102, 126, 234, 0.3);
}

.banner-content {
  position: relative;
  z-index: 2;
}

.welcome-title {
  display: block;
  font-size: 44rpx;
  font-weight: bold;
  color: #fff;
  margin-bottom: 15rpx;
}

.welcome-subtitle {
  display: block;
  font-size: 28rpx;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 10rpx;
}

.welcome-desc {
  display: block;
  font-size: 24rpx;
  color: rgba(255, 255, 255, 0.8);
}

.banner-decoration {
  position: absolute;
  right: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
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

.circle-3 {
  width: 100rpx;
  height: 100rpx;
  right: -20rpx;
  bottom: 50rpx;
}

/* 分区 */
.section {
  margin: 0 30rpx 40rpx;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25rpx;
}

.section-title-wrapper {
  display: flex;
  align-items: center;
}

.section-icon {
  font-size: 36rpx;
  margin-right: 15rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
}

/* 功能网格 */
.function-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20rpx;
}

.function-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 25rpx 10rpx;
  background: #fff;
  border-radius: 16rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.function-card:active {
  transform: scale(0.95);
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.1);
}

.card-icon-wrapper {
  width: 80rpx;
  height: 80rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  margin-bottom: 15rpx;
}

.card-emoji {
  font-size: 40rpx;
}

.card-icon-wrapper.blue {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.card-icon-wrapper.green {
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
}

.card-icon-wrapper.orange {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.card-icon-wrapper.purple {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.card-icon-wrapper.red {
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
}

.card-icon-wrapper.teal {
  background: linear-gradient(135deg, #30cfd0 0%, #330867 100%);
}

.card-icon-wrapper.indigo {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.card-icon-wrapper.gray {
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
}

.card-title {
  font-size: 24rpx;
  color: #666;
  text-align: center;
}
</style>
