from rest_framework import serializers
from transpiled_sql.models import TranspiledSQL

class TranspiledSQLSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranspiledSQL
        fields = ['input_sql', 'output_sql', 'input_dialect', 'output_dialect'
                  , 'is_transpiled', 'errs_msg']
        