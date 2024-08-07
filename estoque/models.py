from django.db import models
from django.utils import timezone

class Alimento(models.Model):
    nome = models.CharField(max_length=100) 
    quantidade = models.IntegerField()
    validade = models.DateField()
    peso = models.DecimalField(max_digits=10, decimal_places=2)

    def esta_vencido(self):
        return self.validade < timezone.now().date()

    def status_validade(self):
        return "Vencido" if self.esta_vencido() else "Válido"
    
    def __str__(self):
        return self.nome

class RegistroEntrada(models.Model):
    alimento = models.ForeignKey(Alimento, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    data_registro = models.DateTimeField(auto_now_add=True)

class RegistroSaida(models.Model):
    alimento = models.ForeignKey(Alimento, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    data_registro = models.DateTimeField(auto_now_add=True)