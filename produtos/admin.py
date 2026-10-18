from django.contrib import admin
from .models import Categoria, Produto, Avaliacao
admin.site.register(Categoria)
admin.site.register(Produto)
admin.site.register(Avaliacao)