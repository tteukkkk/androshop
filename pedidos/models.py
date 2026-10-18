from django.db import models
from django.contrib.auth.models import User
from produtos.models import Produto
from cupons.models import CupomDesconto


class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data_pedido = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('cancelado', 'Cancelado'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pendente')
    cupom = models.ForeignKey(CupomDesconto, null=True, blank=True, on_delete=models.SET_NULL)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    forma_pagamento = models.CharField(
        max_length=20,
        choices=[
            ('credito', 'Cartão de Crédito'),
            ('debito', 'Cartão de Débito'),
            ('pix', 'Pix'),
            ('boleto', 'Boleto'),
        ],
        default='credito'
    )

    def __str__(self):
        return f"Pedido {self.id} - {self.usuario.username}"


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.quantidade * self.preco_unitario
