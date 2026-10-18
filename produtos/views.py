from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Produto, Categoria, Avaliacao
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def lista_produtos(request):
    produtos = Produto.objects.all().order_by('-destaque', 'nome')
    categorias = Categoria.objects.all()
    categoria_id = request.GET.get('categoria')
    preco_min = request.GET.get('preco_min')
    preco_max = request.GET.get('preco_max')
    avaliacao_min = request.GET.get('avaliacao_min')

    if categoria_id:
        produtos = produtos.filter(categoria_id=categoria_id)
    if preco_min:
        produtos = produtos.filter(preco__gte=preco_min)
    if preco_max:
        produtos = produtos.filter(preco__lte=preco_max)
    if avaliacao_min:
        produtos = [p for p in produtos if p.media_avaliacoes() >= int(avaliacao_min)]

    return render(request, 'produtos/lista_produtos.html', {
        'produtos': produtos,
        'categorias': categorias,
        'categoria_ativa': None,
    })


def lista_produtos_categoria(request, slug):
    categoria = get_object_or_404(Categoria, slug=slug)
    produtos = Produto.objects.filter(categoria=categoria).order_by('-destaque', 'nome')
    categorias = Categoria.objects.all()
    return render(request, 'produtos/lista_produtos.html', {
        'produtos': produtos,
        'categorias': categorias,
        'categoria_ativa': categoria,
    })


def detalhe_produto(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    avaliacoes = produto.avaliacoes.all()
    return render(request, 'produtos/detalhe_produto.html', {
        'produto': produto,
        'avaliacoes': avaliacoes,
    })


@login_required
def avaliar_produto(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    usuario = request.user

    if request.method == 'POST':
        nota = request.POST.get('nota')
        comentario = request.POST.get('comentario', '').strip()

        if not nota:
            messages.error(request, 'Por favor, selecione uma nota para avaliar o produto!')
            return redirect('detalhe_produto', produto_id=produto.id)

        try:
            nota = int(nota)
            if nota < 1 or nota > 5:
                raise ValueError
        except (TypeError, ValueError):
            messages.error(request, 'A nota deve ser um número entre 1 e 5!')
            return redirect('detalhe_produto', produto_id=produto.id)

        avaliacao, criado = Avaliacao.objects.get_or_create(
            produto=produto,
            usuario=usuario,
            defaults={'nota': nota, 'comentario': comentario}
        )

        if not criado:
            avaliacao.nota = nota
            avaliacao.comentario = comentario
            avaliacao.save()

        messages.success(request, 'Sua avaliação foi registrada com sucesso!')
        return redirect('detalhe_produto', produto_id=produto.id)

    return redirect('detalhe_produto', produto_id=produto.id)


def buscar_produtos(request):
    query = request.GET.get('q', '')
    produtos = Produto.objects.none()
    if query:
        produtos = Produto.objects.filter(
            Q(nome__icontains=query) | Q(descricao__icontains=query)
        ).order_by('-destaque', 'nome')

    categorias = Categoria.objects.all()
    return render(request, 'produtos/buscar_produtos.html', {
        'produtos': produtos,
        'categorias': categorias,
        'query': query,
    })
