from django.apps import AppConfig


class TranspiledSqlConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "transpiled_sql"
