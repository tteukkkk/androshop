from django.db import migrations
import datetime


def create_andro10(apps, schema_editor):
    Cupom = apps.get_model('cupons', 'CupomDesconto')
    Cupom.objects.update_or_create(
        codigo='ANDRO10',
        defaults={
            'desconto_percentual': '10.00',
            'ativo': True,
            'validade': datetime.date(2100, 1, 1),
        }
    )


class Migration(migrations.Migration):

    dependencies = [
        ('cupons', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_andro10),
    ]
