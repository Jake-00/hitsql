import { request } from '../network/axios'
import type { TranspilationInfoType, NameType } from './data'
import { Text }from"@codemirror/state"

export async function getUserInfo() {
  return request<NameType>('https://www.fastmock.site/mock/ca8533cc667844de72db39a6b8ab925a/quiz/id', {
    params: {
      // id
    },
    method: 'GET' // 'POST'
  })
}

export async function postTransSQL(inputSQL: Text) {
  // return request<TranspilationInfoType>('/', {
  //   data: {
  //     input_sql: inputSQL,
  //     output_sql: '',
  //     input_dialect: 'hive',
  //     output_dialect: 'trino',
  //   },
  //   method: 'POST' // 'POST'
  // })
  return request<TranspilationInfoType>('/transpile', {
    data: {
      input_sql: inputSQL.toString(),  // inputSQL would raise 400
      output_sql: '',
      input_dialect: 'hive',
      output_dialect: 'trino',
    },
    method: 'POST' // 'POST'
  })
}