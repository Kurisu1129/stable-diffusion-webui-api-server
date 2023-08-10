import request from '@/utils/request'

export function getList(params) {
  return request({
    url: '/vue-admin-template/table/list',
    method: 'get',
    params
  })
}
export function upload(data) {
  return request({
    url: '/vue-admin-template/upload',
    method: 'post',
    data
  })
}
