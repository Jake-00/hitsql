from django.db import models
from sqlglot.dialects.dialect import Dialects

SQL_DIALECTS = sorted([(d.lower(), d.lower()) for d in dir(Dialects) if d.isupper() and d != "DIALECT"])

class TranspiledSQL(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    input_sql = models.TextField(default='')
    output_sql = models.TextField(default='')
    input_dialect = models.CharField(choices=SQL_DIALECTS, default='mysql', max_length=10)
    output_dialect = models.CharField(choices=SQL_DIALECTS, default='hive', max_length=10)
    is_transpiled = models.CharField(choices=[('0', '0'), ('1', '1')], default='0', max_length=1)
    errs_msg = models.TextField(default='')
    
    
    class Meta:
        ordering = ['created']