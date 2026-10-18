from django.contrib import admin
from .models import CupomDesconto
@admin.register(CupomDesconto)
class CupomDescontoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'desconto_percentual', 'ativo', 'validade']
    search_fields = ['codigo']
    list_filter = ['ativo', 'validade']