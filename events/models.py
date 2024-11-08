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



class Participante(models.Model):
    nome = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    data_inscricao = models.DateTimeField(auto_now_add=True)
    evento_associado = models.ForeignKey(Evento, on_delete=models.CASCADE)

    def __str__(self):
         return f"{self.nome} - {self.email} / {self.evento_associado}"
