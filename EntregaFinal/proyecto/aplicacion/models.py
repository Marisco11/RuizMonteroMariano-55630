from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Celular(models.Model):
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    precio = models.IntegerField()

    def __str__(self):
        return f"{self.modelo}"

class TV (models.Model):
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    pulgadas = models.IntegerField()
    precio = models.IntegerField()

    def __str__(self):
        return f"{self.modelo}"

class PC (models.Model):
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    procesador = models.CharField(max_length=50)
    disco = models.CharField(max_length=50)
    pulgadas = models.IntegerField()
    precio = models.IntegerField()
    
    def __str__(self):
        return f"{self.modelo}"

class Avatar (models.Model):
    imagen = models.ImageField(upload_to="avatares")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__ (self):
        return f"{self.user} {self.imagen}"