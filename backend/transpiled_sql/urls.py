from django.urls import path
from transpiled_sql import views

urlpatterns = [
    path('transpile', views.transpile_sql_dialect),
]
