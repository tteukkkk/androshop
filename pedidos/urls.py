from django.urls import path
from . import views

urlpatterns = [
    path('carrinho/', views.carrinho, name='carrinho'),
    path('adicionar/<int:produto_id>/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('remover/<int:produto_id>/', views.remover_do_carrinho, name='remover_do_carrinho'),
    path('atualizar/<int:produto_id>/', views.atualizar_quantidade, name='atualizar_quantidade'),
    path('fechar/', views.fechar_pedido, name='fechar_pedido'),
    path('meus/', views.meus_pedidos, name='meus_pedidos'),
    path('confirmar/<int:pedido_id>/', views.confirmar_pagamento, name='confirmar_pagamento'),
]
