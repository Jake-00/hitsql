from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from transpiled_sql.models import TranspiledSQL
from transpiled_sql.serializers import TranspiledSQLSerializer
import sqlglot
import json

@csrf_exempt
def transpile_sql_dialect(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        input_sql = data.get("input_sql", "")
        output_sql = data.get("output_sql", "")
        input_dialect = data.get("input_dialect", "")
        output_dialect = data.get("output_dialect", "")
        is_transpiled = '0'
        errs_msg= ''
        
        try:
            output_sql = sqlglot.transpile(input_sql, read=input_dialect, write=output_dialect, pretty=True)[0]
            is_transpiled = '1'
            errs_msg = '\{\}'
        except sqlglot.errors.ParseError as e:
            output_sql = 'transpilation error'
            errs_msg = json.dumps(e.errors)
            # return JsonResponse(serializer.errors, status=400)
        finally:
            data['output_sql'] = output_sql
            data['errs_msg'] = errs_msg
            data['is_transpiled'] = is_transpiled
            serializer = TranspiledSQLSerializer(data=data)
            # is_valid judgement is necessary
            if serializer.is_valid():
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)