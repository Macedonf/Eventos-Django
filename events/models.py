from django.db import models

#modelo de eventos

class Evento(models.Model):
    nome_evento = models.CharField(max_length=255)
    data_inicio = models.DateField(null=False)
    data_fim = models.DateField(null=True)
    descricao = models.TextField(blank=True, null=True)
    local = models.CharField(max_length=255)

    def __str__(self):
         return f" {self.nome_evento} - {self.data_inicio}/{self.local}"