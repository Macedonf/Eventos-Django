from django.contrib.auth.models import User
from django.db import models

#modelo de eventos

class Evento(models.Model):
    organizador = models.ForeignKey(User, on_delete=models.CASCADE)
    nome_evento = models.CharField(max_length=255)
    data_inicio = models.DateField(null=False)
    data_fim = models.DateField(null=True)
    descricao = models.TextField(blank=True, null=True)
    local = models.CharField(max_length=255)

    def __str__(self):
         return f" {self.nome_evento} - {self.data_inicio}/{self.local}"

    def obter_relatorio(self):
        total_inscritos = self.participante_set.count()
        total_pagantes = self.participante_set.filter(ingresso='PAGO').count()
        total_nao_pagantes = self.participante_set.filter(ingresso='NAO_PAGO').count()
        total_pago = self.participante_set.filter(ingresso='PAGO').aggregate(models.Sum('valor_ingresso'))[
                         'valor_ingresso__sum'] or 0
        return {
            'total_inscritos': total_inscritos,
            'total_pagantes': total_pagantes,
            'total_nao_pagantes': total_nao_pagantes,
            'total_pago': total_pago
        }


class Participante(models.Model):
    PAGO_CHOICES = [
        ('PAGO', 'Pago'),
        ('NAO_PAGO', 'Não Pago'),
    ]

    nome = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    data_inscricao = models.DateTimeField(auto_now_add=True)
    evento_associado = models.ForeignKey(Evento, on_delete=models.CASCADE)
    valor_ingresso= models.DecimalField(max_digits=8, decimal_places=2)
    ingresso = models.CharField(max_length=8, choices=PAGO_CHOICES, default='NAO_PAGO')

    def __str__(self):
        return f"{self.nome} - {self.ingresso}"


