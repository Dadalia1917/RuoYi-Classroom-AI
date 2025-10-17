<template>
  <div class="data-overview-container">
    <el-row :gutter="20">
      <!-- 本日拦截危险行为统计 -->
      <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
        <el-card shadow="hover" class="chart-card">
          <template #header>
            <div class="card-header">
              <span class="card-title">学生行为统计图</span>
            </div>
          </template>
          <div ref="dangerChartRef" class="chart-container"></div>
        </el-card>
      </el-col>

      <!-- 本日用户网站使用率 -->
      <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
        <el-card shadow="hover" class="chart-card">
          <template #header>
            <div class="card-header">
              <span class="card-title">本日用户网站使用率</span>
            </div>
          </template>
          <div ref="usageChartRef" class="chart-container"></div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px;">
      <!-- 近期检测情况 -->
      <el-col :span="24">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span class="card-title">近期检测情况</span>
              <div>
                <el-button type="primary" size="small" @click="refreshData">刷新</el-button>
              </div>
            </div>
          </template>
          <el-table :data="recordsData" stripe style="width: 100%" v-loading="loading">
            <el-table-column prop="id" label="序号" width="80" align="center" />
            <el-table-column prop="username" label="用户名" align="center" />
            <el-table-column prop="weight" label="模型" align="center" />
            <el-table-column label="检测结果" align="center" min-width="200">
              <template #default="scope">
                <span>{{ formatLabel(scope.row.label) }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="startTime" label="检测时间" align="center" width="180" />
            <el-table-column prop="conf" label="置信度阈值" align="center" width="120">
              <template #default="scope">
                <el-tag :type="scope.row.conf >= 0.5 ? 'success' : 'warning'">
                  {{ scope.row.conf }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="type" label="检测类型" align="center">
              <template #default="scope">
                <el-tag v-if="scope.row.type === 'img'" type="primary">图像检测</el-tag>
                <el-tag v-else-if="scope.row.type === 'video'" type="success">视频检测</el-tag>
                <el-tag v-else-if="scope.row.type === 'camera'" type="warning">摄像检测</el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup name="DataOverview">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import * as echarts from 'echarts'
import request from '@/utils/request'

// 图表实例
const dangerChartRef = ref(null)
const usageChartRef = ref(null)
let dangerChart = null
let usageChart = null

// 数据
const recordsData = ref([])
const loading = ref(false)

// 行为标签映射（英文 -> 中文）
const behaviorMap = {
  'Writing': '写作',
  'Reading': '阅读',
  'Listening': '听讲',
  'Sleeping': '睡觉',
  'Discussing': '讨论',
  'Raising_hand': '举手',
  'Bowing': '低头',
  'Phone': '玩手机',
  'Stand': '站立'
}

// 初始化学生行为统计图表
const initDangerChart = () => {
  if (!dangerChartRef.value) return
  
  dangerChart = echarts.init(dangerChartRef.value)
  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    legend: {
      data: ['写作', '阅读', '听讲', '睡觉', '讨论', '举手', '低头', '玩手机', '站立']
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'value'
    },
    yAxis: {
      type: 'category',
      data: ['次数']
    },
    series: [
      { name: '写作', type: 'bar', stack: 'total', data: [0], itemStyle: { color: '#5470c6' } },
      { name: '阅读', type: 'bar', stack: 'total', data: [0], itemStyle: { color: '#91cc75' } },
      { name: '听讲', type: 'bar', stack: 'total', data: [0], itemStyle: { color: '#fac858' } },
      { name: '睡觉', type: 'bar', stack: 'total', data: [0], itemStyle: { color: '#ee6666' } },
      { name: '讨论', type: 'bar', stack: 'total', data: [0], itemStyle: { color: '#73c0de' } },
      { name: '举手', type: 'bar', stack: 'total', data: [0], itemStyle: { color: '#3ba272' } },
      { name: '低头', type: 'bar', stack: 'total', data: [0], itemStyle: { color: '#fc8452' } },
      { name: '玩手机', type: 'bar', stack: 'total', data: [0], itemStyle: { color: '#9a60b4' } },
      { name: '站立', type: 'bar', stack: 'total', data: [0], itemStyle: { color: '#ea7ccc' } }
    ]
  }
  dangerChart.setOption(option)
}

// 初始化使用率饼图
const initUsageChart = () => {
  if (!usageChartRef.value) return
  
  usageChart = echarts.init(usageChartRef.value)
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      right: '10%',
      top: 'center'
    },
    series: [
      {
        name: '用户使用率',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 20,
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: [
          { value: 100, name: 'admin', itemStyle: { color: '#5470c6' } }
        ]
      }
    ]
  }
  usageChart.setOption(option)
}

// 获取检测记录数据
const fetchRecordsData = async () => {
  loading.value = true
  try {
    // 获取所有类型的记录
    const [imgRes, videoRes, cameraRes] = await Promise.all([
      request.get('/imgRecords/all').catch(() => ({ data: [] })),
      request.get('/videoRecords/all').catch(() => ({ data: [] })),
      request.get('/cameraRecords/all').catch(() => ({ data: [] }))
    ])

    const imgRecords = (imgRes.data || []).map(item => ({ ...item, type: 'img' }))
    const videoRecords = (videoRes.data || []).map(item => ({ ...item, type: 'video' }))
    const cameraRecords = (cameraRes.data || []).map(item => ({ ...item, type: 'camera' }))

    // 合并所有记录并按时间排序
    const allRecords = [...imgRecords, ...videoRecords, ...cameraRecords]
    allRecords.sort((a, b) => {
      return new Date(b.startTime || 0) - new Date(a.startTime || 0)
    })

    recordsData.value = allRecords.slice(0, 10) // 只显示最近10条

    // 更新图表数据
    updateCharts(allRecords)
  } catch (error) {
    console.error('获取记录数据失败:', error)
  } finally {
    loading.value = false
  }
}

// 更新图表数据
const updateCharts = (records) => {
  // 统计今日行为数据
  const today = new Date().toISOString().split('T')[0]
  const todayRecords = records.filter(r => r.startTime && r.startTime.startsWith(today))

  // 统计各类行为
  const behaviorCount = {
    Writing: 0,
    Reading: 0,
    Listening: 0,
    Sleeping: 0,
    Discussing: 0,
    Raising_hand: 0,
    Bowing: 0,
    Phone: 0,
    Stand: 0
  }

  todayRecords.forEach(record => {
    // 解析label字段（可能是字符串或数组）
    let labels = []
    if (record.label) {
      if (typeof record.label === 'string') {
        try {
          // 尝试解析JSON字符串
          labels = JSON.parse(record.label)
        } catch {
          // 如果不是JSON，直接作为字符串处理
          labels = [record.label]
        }
      } else if (Array.isArray(record.label)) {
        labels = record.label
      }
    }

    // 统计每种行为出现的次数（包括英文和中文标签）
    labels.forEach(label => {
      const labelStr = String(label)
      
      // 检查英文标签
      if (labelStr.includes('Writing')) behaviorCount.Writing++
      else if (labelStr.includes('Reading')) behaviorCount.Reading++
      else if (labelStr.includes('Listening')) behaviorCount.Listening++
      else if (labelStr.includes('Sleeping')) behaviorCount.Sleeping++
      else if (labelStr.includes('Discussing')) behaviorCount.Discussing++
      else if (labelStr.includes('Raising_hand')) behaviorCount.Raising_hand++
      else if (labelStr.includes('Bowing')) behaviorCount.Bowing++
      else if (labelStr.includes('Phone')) behaviorCount.Phone++
      else if (labelStr.includes('Stand')) behaviorCount.Stand++
      // 检查中文标签
      else if (labelStr.includes('写作')) behaviorCount.Writing++
      else if (labelStr.includes('阅读')) behaviorCount.Reading++
      else if (labelStr.includes('听讲')) behaviorCount.Listening++
      else if (labelStr.includes('睡觉')) behaviorCount.Sleeping++
      else if (labelStr.includes('讨论')) behaviorCount.Discussing++
      else if (labelStr.includes('举手')) behaviorCount.Raising_hand++
      else if (labelStr.includes('低头')) behaviorCount.Bowing++
      else if (labelStr.includes('玩手机')) behaviorCount.Phone++
      else if (labelStr.includes('站立')) behaviorCount.Stand++
    })
  })

  console.log('今日行为统计:', behaviorCount)

  // 更新柱状图
  if (dangerChart) {
    dangerChart.setOption({
      series: [
        { data: [behaviorCount.Writing] },
        { data: [behaviorCount.Reading] },
        { data: [behaviorCount.Listening] },
        { data: [behaviorCount.Sleeping] },
        { data: [behaviorCount.Discussing] },
        { data: [behaviorCount.Raising_hand] },
        { data: [behaviorCount.Bowing] },
        { data: [behaviorCount.Phone] },
        { data: [behaviorCount.Stand] }
      ]
    })
  }

  // 统计用户使用率
  const userStats = {}
  todayRecords.forEach(record => {
    const username = record.username || 'unknown'
    userStats[username] = (userStats[username] || 0) + 1
  })

  const pieData = Object.keys(userStats).map(username => ({
    value: userStats[username],
    name: username
  }))

  // 更新饼图
  if (usageChart) {
    usageChart.setOption({
      series: [{
        data: pieData.length > 0 ? pieData : [{ value: 100, name: 'admin' }]
      }]
    })
  }
}

// 格式化标签（英文转中文，保留所有标签不去重）
const formatLabel = (label) => {
  if (!label) return '-'
  
  let labels = []
  if (typeof label === 'string') {
    try {
      // 先尝试JSON解析（会自动解码 \uXXXX）
      const parsed = JSON.parse(label)
      if (Array.isArray(parsed)) {
        labels = parsed
      } else {
        labels = [parsed]
      }
      console.log('JSON.parse成功:', label, '→', labels)
    } catch (e) {
      console.warn('JSON.parse失败:', label, e.message)
      // 如果解析失败，可能是双重转义，尝试处理
      try {
        // 替换双重转义的反斜杠
        const unescaped = label.replace(/\\\\u/g, '\\u')
        const parsed2 = JSON.parse(unescaped)
        if (Array.isArray(parsed2)) {
          labels = parsed2
        } else {
          labels = [parsed2]
        }
        console.log('二次解析成功:', unescaped, '→', labels)
      } catch (e2) {
        console.warn('二次解析也失败，使用原字符串:', e2.message)
        labels = [label]
      }
    }
  } else if (Array.isArray(label)) {
    labels = label
    console.log('label已经是数组:', labels)
  } else {
    return '-'
  }

  // 翻译成中文（不去重，保留所有标签）
  const translatedLabels = []
  labels.forEach(l => {
    if (!l) return
    
    let labelStr = String(l)
    
    // 匹配英文标签并翻译
    let translated = false
    for (const [en, cn] of Object.entries(behaviorMap)) {
      if (labelStr.includes(en)) {
        translatedLabels.push(cn)
        translated = true
        break
      }
    }
    
    // 如果没有匹配到英文标签，检查是否已经是中文
    if (!translated && labelStr) {
      // 检查是否在behaviorMap的值中
      const isChineseLabel = Object.values(behaviorMap).includes(labelStr)
      if (isChineseLabel) {
        translatedLabels.push(labelStr)
      } else {
        // 不是已知标签，直接显示（可能是乱码或未知标签）
        console.warn('未识别的标签:', labelStr)
        translatedLabels.push(labelStr)
      }
    }
  })

  const result = translatedLabels.length > 0 ? translatedLabels.join(', ') : '-'
  console.log('formatLabel最终结果:', label, '→', result)
  return result
}

// 刷新数据
const refreshData = () => {
  fetchRecordsData()
}

// 响应式调整图表大小
const handleResize = () => {
  dangerChart?.resize()
  usageChart?.resize()
}

onMounted(() => {
  initDangerChart()
  initUsageChart()
  fetchRecordsData()
  window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
  dangerChart?.dispose()
  usageChart?.dispose()
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped lang="scss">
.data-overview-container {
  padding: 20px;
}

.chart-card {
  height: 400px;
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    
    .card-title {
      font-size: 16px;
      font-weight: 600;
      color: #303133;
    }
  }
}

.chart-container {
  width: 100%;
  height: 320px;
}

:deep(.el-card__body) {
  height: calc(100% - 60px);
}
</style>

