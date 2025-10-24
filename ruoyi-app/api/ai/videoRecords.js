import request from '@/utils/request'

// 查询视频记录列表
export function listVideoRecords(query) {
  return request({
    url: '/videoRecords/all',
    method: 'get',
    params: query
  })
}

// 查询视频记录详细
export function getVideoRecords(id) {
  return request({
    url: '/videoRecords/' + id,
    method: 'get'
  })
}

// 新增视频记录
export function addVideoRecords(data) {
  return request({
    url: '/videoRecords/save',
    method: 'post',
    data: data
  })
}

// 修改视频记录
export function updateVideoRecords(data) {
  return request({
    url: '/videoRecords/updates',
    method: 'put',
    data: data
  })
}

// 删除视频记录
export function delVideoRecords(id) {
  return request({
    url: '/videoRecords/delete/' + id,
    method: 'delete'
  })
}