from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone
from produtos.models import Produto, Categoria
from cupons.models import CupomDesconto
from .models import Pedido

class CarrinhoTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('demo',password='teste-local-123')
        self.client.force_login(self.user)
        cat=Categoria.objects.create(nome='Celulares',slug='celulares')
        self.produto=Produto.objects.create(nome='Celular',descricao='Demo',preco=Decimal('100.00'),estoque=2,categoria=cat,imagem='produtos/demo.png')
        sess=self.client.session; sess['carrinho']={str(self.produto.pk):1};sess.save()

    def test_pedido_com_cupom(self):
        CupomDesconto.objects.create(codigo='DEMO10', desconto_percentual=10, ativo=True, validade=timezone.localdate()+timedelta(days=1))
        self.client.post(reverse('fechar_pedido'),{'acao':'finalizar','cupom':'DEMO10'})
        self.assertEqual(Pedido.objects.get().total, Decimal('90.00'))
        self.produto.refresh_from_db(); self.assertEqual(self.produto.estoque,1)

    def test_estoque_insuficiente_nao_gera_pedido(self):
        sess=self.client.session;sess['carrinho']={str(self.produto.pk):3};sess.save()
        self.client.post(reverse('fechar_pedido'),{'acao':'finalizar'})
        self.assertFalse(Pedido.objects.exists())
        self.produto.refresh_from_db();self.assertEqual(self.produto.estoque,2)

    def test_quantidade_invalida_nao_quebra_pagina(self):
        self.assertEqual(self.client.post(reverse('atualizar_quantidade',args=[self.produto.pk]),{'quantidade':'abc'}).status_code,302)

    def test_paginas_loja(self):
        for name in ['home','lista_produtos','carrinho','meus_pedidos']:
            with self.subTest(name=name):self.assertEqual(self.client.get(reverse(name)).status_code,200)
