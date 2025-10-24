import request from '@/utils/request'

// 获取模型列表
export function getModelList() {
  return request({
    url: '/flask/file_names',
    method: 'get'
  })
}

// 图像预测
export function predictImage(data) {
  return request({
    url: '/flask/predictImg',
    method: 'post',
    data: data,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// 视频预测
export function predictVideo(data) {
  return request({
    url: '/flask/predictVideo',
    method: 'post',
    data: data,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// 摄像头预测
export function predictCamera(data) {
  return request({
    url: '/flask/predictCamera',
    method: 'post',
    data: data
  })
}

// 停止摄像头
export function stopCamera() {
  return request({
    url: '/flask/stopCamera',
    method: 'get'
  })
}