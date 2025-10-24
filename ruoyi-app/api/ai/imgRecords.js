import request from '@/utils/request'

// 查询图片记录列表
export function listImgRecords(query) {
  return request({
    url: '/imgRecords/all',
    method: 'get',
    params: query
  })
}

// 查询图片记录详细
export function getImgRecords(id) {
  return request({
    url: '/imgRecords/' + id,
    method: 'get'
  })
}

// 新增图片记录
export function addImgRecords(data) {
  return request({
    url: '/imgRecords/save',
    method: 'post',
    data: data
  })
}

// 修改图片记录
export function updateImgRecords(data) {
  return request({
    url: '/imgRecords/updates',
    method: 'put',
    data: data
  })
}

// 删除图片记录
export function delImgRecords(id) {
  return request({
    url: '/imgRecords/delete/' + id,
    method: 'delete'
  })
}