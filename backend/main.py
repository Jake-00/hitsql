from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
import sqlglot
import json
from transpile_tools import customized_transpile


class Item(BaseModel):
    input_sql: str
    output_sql: str | None = None
    input_dialect: str | None = 'hive'
    output_dialect: str | None = 'trino'
    is_transpile: str | None = '0'
    err_msg: str | None = '\{\}'
    
class DialectsInfo(BaseModel):
    dialects_info: str

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}


@app.post("/transpile")
def transpile(item: Item):
    output_sql = ''
    is_transpiled = '0'
    err_msg = '\{\}'
    try:
        output_sql = sqlglot.transpile(item.input_sql, read=item.input_dialect, write=item.output_dialect, pretty=True)[0]
        is_transpiled = '1'
    except sqlglot.errors.ParseError as e:
        err_msg = e.errors
    else:
        item.output_sql = customized_transpile(item.input_sql, item.input_dialect, 
                                               output_sql, item.output_dialect)

    item.is_transpile = is_transpiled
    item.err_msg = err_msg
    return item

@app.get("/get_dialects")
def get_dialects_info():
    dialects_upper = list(sqlglot.Dialects.__members__.keys())
    dialect_objs_arr = [
            {
                'value': dialect_upper.lower(),
                'label': dialect_upper.lower(),
                'other': 'extra'
            } for dialect_upper in dialects_upper]
    dialects_json = json.dumps(dialect_objs_arr)
    dialects_info = DialectsInfo()
    dialects_info.dialects_info = dialects_json
    return dialects_info