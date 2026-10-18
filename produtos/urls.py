from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_produtos, name='lista_produtos'),
    path('categoria/<slug:slug>/', views.lista_produtos_categoria, name='lista_produtos_categoria'),
    path('buscar/', views.buscar_produtos, name='buscar_produtos'),
    path('<int:produto_id>/', views.detalhe_produto, name='detalhe_produto'),
    path('<int:produto_id>/avaliar/', views.avaliar_produto, name='avaliar_produto'),
]
