import request from '@/utils/request'

// 查询摄像记录列表
export function listCameraRecords(query) {
  return request({
    url: '/cameraRecords/all',
    method: 'get',
    params: query
  })
}

// 查询摄像记录详细
export function getCameraRecords(id) {
  return request({
    url: '/cameraRecords/' + id,
    method: 'get'
  })
}

// 新增摄像记录
export function addCameraRecords(data) {
  return request({
    url: '/cameraRecords/save',
    method: 'post',
    data: data
  })
}

// 修改摄像记录
export function updateCameraRecords(data) {
  return request({
    url: '/cameraRecords/updates',
    method: 'put',
    data: data
  })
}

// 删除摄像记录
export function delCameraRecords(id) {
  return request({
    url: '/cameraRecords/delete/' + id,
    method: 'delete'
  })
}
