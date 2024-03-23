from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
import sqlglot


class Item(BaseModel):
    input_sql: str
    output_sql: str | None = None
    input_dialect: str | None = 'hive'
    output_dialect: str | None = 'trino'
    is_transpile: str | None = '0'
    err_msg: str | None = '\{\}'

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/transpile")
def transpile(item: Item):
    output_sql = ''
    is_transpiled = '0'
    err_msg = '\{\}'
    try:
        output_sql = sqlglot.transpile(item.input_sql, read=item.input_dialect, write=item.output_dialect)[0]
        is_transpiled = '1'
    except sqlglot.errors.ParseError as e:
        err_msg = e.errors
    item.output_sql = output_sql

    item.is_transpile = is_transpiled
    item.err_msg = err_msg
    return item