<template>
  <view class="about-container">
    <view class="header-section text-center">
      <view class="logo-icon">🎓</view>
      <uni-title type="h2" title="课堂行为分析系统"></uni-title>
    </view>

    <view class="content-section">
      <view class="menu-list">
        <view class="list-cell list-cell-arrow">
          <view class="menu-item-box">
            <view>版本信息</view>
            <view class="text-right">v{{version}}</view>
          </view>
        </view>
        <view class="list-cell list-cell-arrow">
          <view class="menu-item-box">
            <view>官方邮箱</view>
            <view class="text-right">support@classroom-ai.com</view>
          </view>
        </view>
        <view class="list-cell list-cell-arrow">
          <view class="menu-item-box">
            <view>服务热线</view>
            <view class="text-right">400-888-8888</view>
          </view>
        </view>
        <view class="list-cell list-cell-arrow">
          <view class="menu-item-box">
            <view>公司网站</view>
            <view class="text-right">
              <uni-link :href="url" :text="url" showUnderLine="false"></uni-link>
            </view>
          </view>
        </view>
      </view>
    </view>

    <view class="copyright">
      <view>Copyright &copy; 2025 课堂行为分析系统 All Rights Reserved.</view>
    </view>
  </view>
</template>

<script setup>
  import { useConfigStore } from '@/store'

  const url = useConfigStore().config.appInfo.site_url
  const version = useConfigStore().config.appInfo.version
</script>

<style lang="scss" scoped>
  page {
    background-color: #f8f8f8;
  }

  .copyright {
    margin-top: 50rpx;
    text-align: center;
    line-height: 60rpx;
    color: #999;
  }

  .logo-icon {
    font-size: 150rpx;
    margin: 20rpx 0;
  }

  .header-section {
    display: flex;
    padding: 30rpx 0 0;
    flex-direction: column;
    align-items: center;
  }
</style>
