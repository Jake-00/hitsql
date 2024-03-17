export type NameType = {
    desc: string
}

export type TranspilationInfoType = {
    // code: number,
    // msg: string,
    // data: {
        
    // }
    input_sql: string,
    output_sql: string,
    input_dialect: string,
    output_dialect: string,
    is_transpiled: string,
    errs_msg: string
}
