from django.db import models


class CupomDesconto(models.Model):
    codigo = models.CharField('Código do cupom', max_length=20, unique=True)
    desconto_percentual = models.DecimalField('Desconto (%)', max_digits=5, decimal_places=2, help_text='Exemplo: 10 para 10%')
    ativo = models.BooleanField('Ativo?', default=True)
    validade = models.DateField('Validade')

    def __str__(self):
        return f"{self.codigo} ({self.desconto_percentual}%)"
