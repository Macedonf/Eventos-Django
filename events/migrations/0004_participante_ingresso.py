# Generated by Django 5.1.2 on 2024-11-11 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_evento_organizador'),
    ]

    operations = [
        migrations.AddField(
            model_name='participante',
            name='ingresso',
            field=models.CharField(choices=[('PAGO', 'Pago'), ('NAO_PAGO', 'Não Pago')], default='NAO_PAGO', max_length=8),
        ),
    ]
