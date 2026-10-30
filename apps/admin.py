from django.contrib import admin

from apps.models import Calculation


@admin.register(Calculation)
class CalculationAdmin(admin.ModelAdmin):
    list_display = ('id', 'operation', 'n1', 'n2', 'result', 'created_at')
    list_filter = ('operation',)
    search_fields = ('operation',)