import { request } from '../network/axios'
import type { TranspilationInfoType, DialectsInfoType } from './data'
import { Text }from"@codemirror/state"

// == setup service == //
export function getDialectsList() {
  const DIALECTS_INFO = new Array()
  const DIALECTS_MAP = new Array<Array<string>>(
    ["Athena" , "athena"],
    ["BigQuery" , "bigquery"],
    ["ClickHouse" , "clickhouse"],
    ["Databricks" , "databricks"],
    ["Doris" , "doris"],
    ["Drill" , "drill"],
    ["DuckDB" , "duckdb"],
    ["Hive" , "hive"],  // 8
    ["MySQL" , "mysql"],
    ["Oracle" , "oracle"],
    ["Postgres" , "postgres"],
    ["Presto" , "presto"],  // 12
    ["PRQL" , "prql"],
    ["Redshift" , "redshift"],
    ["Snowflake" , "snowflake"],
    ["Spark" , "spark"],
    ["Spark2" , "spark2"],
    ["SQLite" , "sqlite"],
    ["StarRocks" , "starrocks"],
    ["Tableau" , "tableau"],
    ["Teradata" , "teradata"],
    ["Trino" , "trino"],
    ["TSQL" , "tsql"]
  )
  DIALECTS_MAP.forEach(
    (arr: Array<string>) => {
      DIALECTS_INFO.push(
        {
          value: arr[1],
          label: arr[0],
          other: 'extra'
        }
      )
    }
  )

  return DIALECTS_INFO
}

// == user service == //
export async function postTransSQL(is_llm: boolean, inputSQL: Text, input_dialect: string, output_dialect: string) {
  const req_api = !is_llm ? '/transpile' : '/transpile-llm';
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