from django.db import models
from django.contrib.auth.models import User # Importa o modelo de usuário padrão do Django

# ---------- Categoria ----------
class Categoria(models.Model):
    nome = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.nome
    # Cada categoria representa um grupo, ex: "Celulares Android", "Fones de Ouvido", etc.

# ---------- Produto ----------
class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    imagem = models.ImageField(upload_to='produtos/') # Salva a imagem em /media/produtos/
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='produtos')
    destaque = models.BooleanField(default=False) # Marcar produto como destaque
    estoque = models.PositiveIntegerField(default=0) # Quantos itens em estoque
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome

    def media_avaliacoes(self):
        avaliacoes = self.avaliacoes.all()
        if avaliacoes.exists():
            return round(sum(a.nota for a in avaliacoes) / avaliacoes.count(), 1)
        return 0

    def qtd_avaliacoes(self):
        return self.avaliacoes.count()

# ---------- Avaliação ----------
class Avaliacao(models.Model):
    produto = models.ForeignKey(Produto, related_name='avaliacoes', on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nota = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)]) # 1 a 5 estrelas
    comentario = models.TextField(blank=True)
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('produto', 'usuario') # Um usuário só pode avaliar cada produto uma vez!
        ordering = ['-data'] # Avaliações mais recentes primeiro

    def __str__(self):
        return f"{self.usuario.username} - {self.produto.nome} ({self.nota} estrelas)"
