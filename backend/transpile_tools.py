from sqlglot import Dialects, parse_one, Tokenizer
from sqlglot.tokens import Token
from typing import *


def get_unmatched_tokens_seq(read_tokens: List[str],
                              write_tokens: List[str],
                              read_tokens_org_idx: Tuple[int, int],
                              write_tokens_org_idx: Tuple[int, int],
                              read_unmatched_lst: List[Tuple[int, int]], 
                              write_unmatched_lst: List[Tuple[int, int]]):
    if len(read_tokens) == 0 and len(write_tokens) == 0:
        return
    dp = [[0 for i in range(len(write_tokens) + 1)] for i in range(len(read_tokens) + 1)]
    max_len = 0
    read_end_idx = 0
    write_end_idx = 0
    for i in range(1, len(read_tokens) + 1):
        for j in range(1, len(write_tokens) + 1):
            if read_tokens[i-1] == write_tokens[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
                if dp[i][j] > max_len:
                    max_len = dp[i][j]
                    read_end_idx = i
                    write_end_idx = j
    
    if max_len <= 1:
        in_unmatched_tokens_idx, out_unmatched_tokens_idx = unmatched_tokens_prune(read_tokens, 
                                                                                   write_tokens, 
                                                                                   read_tokens_org_idx, write_tokens_org_idx)
        read_unmatched_lst += in_unmatched_tokens_idx
        write_unmatched_lst += out_unmatched_tokens_idx
        return
    
    read_start_idx = read_end_idx - max_len
    write_start_idx = write_end_idx - max_len
    # left node
    read_left_node_abs_pos = (0 + read_tokens_org_idx[0], 
                              read_start_idx + read_tokens_org_idx[0], )
    write_left_node_abs_pos = (0 + write_tokens_org_idx[0], 
                               write_start_idx + write_tokens_org_idx[0], )
    get_unmatched_tokens_seq(
        read_tokens[0: read_start_idx],
        write_tokens[0: write_start_idx],
        # calculate absolute position in original tokens before slicing
        read_left_node_abs_pos,
        write_left_node_abs_pos,
        read_unmatched_lst, write_unmatched_lst
    )
    # right node
    read_right_node_abs_pos = (read_end_idx + read_tokens_org_idx[0],
                               read_tokens_org_idx[1], )
    write_right_node_abs_pos = (write_end_idx + write_tokens_org_idx[0],
                                write_tokens_org_idx[1], )
    get_unmatched_tokens_seq(
        read_tokens[read_end_idx: len(read_tokens)],
        write_tokens[write_end_idx: len(write_tokens)],
        read_right_node_abs_pos,
        write_right_node_abs_pos,
        read_unmatched_lst, write_unmatched_lst
    )

def unmatched_tokens_prune(read_tokens
                           , write_tokens
                           , read_tokens_org_idx
                           , write_tokens_org_idx):
    in_tokens_len = read_tokens_org_idx[1]-read_tokens_org_idx[0]
    out_tokens_len = write_tokens_org_idx[1]-write_tokens_org_idx[0]
    if in_tokens_len != out_tokens_len:
        return ([read_tokens_org_idx], [write_tokens_org_idx], )
    # token by token replacement
    # range_idx
    in_unmatched_tokens_idx_lst, out_unmatched_tokens_idx_lst = [], []
    for idx, read_token in enumerate(read_tokens):
        if read_token != write_tokens[idx]:
            in_unmatched_tokens_idx_lst.append(
                (read_tokens_org_idx[0] + idx, read_tokens_org_idx[0] + idx + 1, )
            )
            out_unmatched_tokens_idx_lst.append(
                (write_tokens_org_idx[0] + idx, write_tokens_org_idx[0] + idx + 1, )
            )
    return (in_unmatched_tokens_idx_lst, out_unmatched_tokens_idx_lst, )

def get_tokens_lst(sql_dialect, sql):
    POSTGRES_LIKE_DIALECTS = ['postgres', 'duckdb', 'presto', 'trino']
    identifier_replace_flag = False 
    if sql_dialect in POSTGRES_LIKE_DIALECTS:
        identifier_replace_flag = True
        sql = sql.replace('"', '`')
    return (Tokenizer().tokenize(sql), identifier_replace_flag, )

def get_tokens_text_lst(replace_flag, tokens_lst: List[Token]):
    if not replace_flag:
        return [token.text.lower() for token in tokens_lst]
    
    tokens_text_lst = []
    for token in tokens_lst:
        token_text = token.text.lower()
        if token_text == '`':
            tokens_text_lst.append('"')
        else:
            tokens_text_lst.append(token_text)
    return tokens_text_lst

def replace_sql_tokens(
    read_sql, 
    write_sql,
    read_tokens_lst,
    write_tokens_lst,
    read_unmatched_lst, write_unmatched_lst
):
    read_unmatched_lst.reverse()
    write_unmatched_lst.reverse()
    for read_tokens_idx, write_tokens_idx in zip(read_unmatched_lst, write_unmatched_lst):
        # get unmatched tokens positions from Token's
        read_tokens_len = len(read_tokens_lst)
        write_tokens_len = len(write_tokens_lst)
        read_tokens_start, read_tokens_end = read_tokens_idx
        write_tokens_start, write_tokens_end = write_tokens_idx
        if read_tokens_start == read_tokens_len and write_tokens_start < write_tokens_len:
            write_unmatched_org_start_idx = write_tokens_lst[write_tokens_start].start
            write_unmatched_org_end_idx = write_tokens_lst[write_tokens_end-1].end
            # for formatting
            if read_sql[-1] == '\n':
                read_sql = read_sql[:-1] + ' '
            elif read_sql[-1] != ' ':
                read_sql += ' '
            read_sql = read_sql + write_sql[write_unmatched_org_start_idx:write_unmatched_org_end_idx+1]
            # for formatting
            if read_sql[-1] != '\n':
                read_sql += '\n'
        elif read_tokens_start < read_tokens_len and write_tokens_start == write_tokens_len:
            read_sql = read_sql 
        else:
            read_unmatched_org_start_idx = read_tokens_lst[read_tokens_start].start
            read_unmatched_org_end_idx = read_tokens_lst[read_tokens_end-1].end     # read_tokens_end-1
            write_unmatched_org_start_idx = write_tokens_lst[write_tokens_start].start
            write_unmatched_org_end_idx = write_tokens_lst[write_tokens_end-1].end  # write_tokens_end-1
            
            # if len(read_sql[:read_unmatched_org_start_idx]) >= 1 and read_sql[read_unmatched_org_start_idx-1]:
            #     first_part = read_sql[:read_unmatched_org_start_idx]+' '
            # else:
            first_part = read_sql[:read_unmatched_org_start_idx]
            second_part = write_sql[write_unmatched_org_start_idx:write_unmatched_org_end_idx+1]
            third_part = read_sql[read_unmatched_org_end_idx+1:]
            read_sql = first_part + second_part + third_part
        
    return read_sql

def customized_transpile(input_sql: str,
                         input_dialect: str,
                         output_sql: str,
                         output_dialect: str,):
    read_tokens_lst, read_tokens_change_flag = get_tokens_lst(input_dialect, input_sql)
    write_tokens_lst, write_tokens_change_flag = get_tokens_lst(output_dialect, output_sql)
    read_tokens_text_lst = get_tokens_text_lst(read_tokens_change_flag, read_tokens_lst)
    write_tokens_text_lst = get_tokens_text_lst(write_tokens_change_flag, write_tokens_lst)
    read_unmatched_lst, write_unmatched_lst = [], []
    read_tokens_org_idx = (0, len(read_tokens_text_lst), )
    write_tokens_org_idx = (0, len(write_tokens_text_lst), )
    get_unmatched_tokens_seq(read_tokens_text_lst, write_tokens_text_lst,
                            read_tokens_org_idx, write_tokens_org_idx,
                            read_unmatched_lst, write_unmatched_lst)
    transpile_sql = replace_sql_tokens(input_sql, 
                                   output_sql,
                                   read_tokens_lst,
                                   write_tokens_lst,
                                   read_unmatched_lst, write_unmatched_lst)
    return transpile_sql