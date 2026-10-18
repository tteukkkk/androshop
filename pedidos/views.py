from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
from decimal import Decimal
from produtos.models import Produto
from cupons.models import CupomDesconto
from .models import Pedido, ItemPedido


def _inicia_carrinho(request):
    if 'carrinho' not in request.session:
        request.session['carrinho'] = {}
    return request.session['carrinho']


def carrinho(request):
    carrinho = request.session.get('carrinho', {})
    produtos = []
    total = 0

    for produto_id, quantidade in carrinho.items():
        produto = get_object_or_404(Produto, pk=int(produto_id))
        subtotal = produto.preco * quantidade
        produtos.append({'produto': produto, 'quantidade': quantidade, 'subtotal': subtotal})
        total += subtotal

    return render(request, 'pedidos/carrinho.html', {'produtos': produtos, 'total': total})


def adicionar_ao_carrinho(request, produto_id):
    carrinho = _inicia_carrinho(request)
    produto_id = str(produto_id)
    carrinho[produto_id] = carrinho.get(produto_id, 0) + 1
    request.session['carrinho'] = carrinho
    messages.success(request, 'Produto adicionado ao carrinho!')
    return redirect('carrinho')


def remover_do_carrinho(request, produto_id):
    carrinho = _inicia_carrinho(request)
    produto_id = str(produto_id)
    if produto_id in carrinho:
        del carrinho[produto_id]
        request.session['carrinho'] = carrinho
        messages.success(request, 'Produto removido do carrinho!')
    return redirect('carrinho')


def atualizar_quantidade(request, produto_id):
    if request.method == 'POST':
        try:
            quantidade = int(request.POST.get('quantidade', 1))
        except (TypeError, ValueError):
            messages.error(request, 'Quantidade inválida.')
            return redirect('carrinho')
        carrinho = _inicia_carrinho(request)
        produto_id = str(produto_id)
        if quantidade > 0:
            carrinho[produto_id] = quantidade
        else:
            carrinho.pop(produto_id, None)
        request.session['carrinho'] = carrinho
        messages.success(request, 'Quantidade atualizada!')
    return redirect('carrinho')


@login_required
def fechar_pedido(request):
    carrinho = request.session.get('carrinho', {})
    if not carrinho:
        messages.error(request, 'Seu carrinho está vazio.')
        return redirect('carrinho')

    produtos_carrinho = []
    total = 0
    for produto_id, quantidade in carrinho.items():
        produto = get_object_or_404(Produto, pk=int(produto_id))
        subtotal = produto.preco * quantidade
        produtos_carrinho.append({'produto': produto, 'quantidade': quantidade, 'subtotal': subtotal})
        total += subtotal

    desconto = 0
    cupom_aplicado = None
    cupom_codigo = ''

    if request.method == 'POST':
        acao = request.POST.get('acao')
        forma_pagamento = request.POST.get('forma_pagamento', 'credito')
        cupom_codigo = request.POST.get('cupom', '').strip()

        if cupom_codigo:
            try:
                cupom = CupomDesconto.objects.get(
                    codigo__iexact=cupom_codigo,
                    ativo=True,
                    validade__gte=timezone.localdate(),
                )
                desconto = (min(Decimal('100'), max(Decimal('0'), cupom.desconto_percentual)) / Decimal('100')) * total
                cupom_aplicado = cupom
                messages.success(request, f"Cupom '{cupom_codigo}' aplicado com sucesso!")
            except CupomDesconto.DoesNotExist:
                messages.error(request, 'Cupom inválido ou expirado.')

        total_final = total - desconto

        if acao == 'finalizar':
            with transaction.atomic():
                produtos_bloqueados = {p.id: p for p in Produto.objects.select_for_update().filter(pk__in=[i['produto'].pk for i in produtos_carrinho]).order_by('id')}
                if any(i['quantidade'] <= 0 or produtos_bloqueados[i['produto'].pk].estoque < i['quantidade'] for i in produtos_carrinho):
                    messages.error(request, 'Estoque insuficiente.')
                    return redirect('carrinho')
                pedido = Pedido.objects.create(
                    usuario=request.user,
                    status='pendente',
                    cupom=cupom_aplicado,
                    total=total_final,
                    forma_pagamento=forma_pagamento,
                )
                for item in produtos_carrinho:
                    ItemPedido.objects.create(
                        pedido=pedido,
                        produto=item['produto'],
                        quantidade=item['quantidade'],
                        preco_unitario=item['produto'].preco,
                    )
                    produto = produtos_bloqueados[item['produto'].pk]
                    produto.estoque -= item['quantidade']
                    produto.save(update_fields=['estoque'])
    
            del request.session['carrinho']
            messages.success(request, 'Pedido realizado com sucesso!')
            return redirect('meus_pedidos')
    else:
        total_final = total

    return render(request, 'pedidos/fechar_pedido.html', {
        'produtos': produtos_carrinho,
        'total': total,
        'desconto': desconto,
        'total_final': total_final,
        'cupom_codigo': cupom_codigo,
    })


@login_required
def confirmar_pagamento(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id, usuario=request.user)
    if pedido.status == 'pendente':
        pedido.status = 'pago'
        pedido.save()
        messages.success(request, 'Pagamento confirmado com sucesso!')
    else:
        messages.info(request, 'Pedido já está pago ou cancelado.')
    return redirect('meus_pedidos')


@login_required
def meus_pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-data_pedido')
    return render(request, 'pedidos/meus_pedidos.html', {'pedidos': pedidos})
