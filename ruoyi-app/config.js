// 应用全局配置
export default {
  baseUrl: 'http://localhost:9999',
  // baseUrl: 'https://vue.ruoyi.vip/prod-api',
  // 应用信息
  appInfo: {
    // 应用名称
    name: "课堂行为检测App",
    // 应用版本
    version: "1.2.0",
    // 应用logo
    logo: "/static/logo.png",
    // 官方网站
    site_url: "http://classroom-ai.com",
    // 政策协议
    agreements: [{
        title: "隐私政策",
        url: "/static/protocol/privacy-policy.html"
      },
      {
        title: "用户服务协议",
        url: "/static/protocol/user-agreement.html"
      }
    ]
  }
}
