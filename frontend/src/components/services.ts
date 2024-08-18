import { request } from '../network/axios'
import type { TranspilationInfoType, DialectsInfoType } from './data'
import { Text }from"@codemirror/state"

// == setup service == //
export function getDialectsList() {
  return [{
    value: 'hive',
    label: 'Hive',
    other: 'extra'
  }, {
    value: 'presto',
    label: 'Presto',
    other: 'extra'
  }]
}

// == user service == //
export async function postTransSQL(is_llm: boolean, inputSQL: Text, input_dialect: string, output_dialect: string) {
  const req_api = is_llm ? '/transpile' : '/transpile-llm';
  return request<TranspilationInfoType>(req_api, {
      data: {
        input_sql: inputSQL.toString(),  // inputSQL would raise 400
        output_sql: '',
        input_dialect: input_dialect,
        output_dialect: output_dialect,
      },
      method: 'POST'
    })
}