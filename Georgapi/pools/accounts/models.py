from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.conf import settings
from utils import Plan_status,Tipo,Tipo_usuario

# Criando o modelos de empresas 
class Empresas(models.Model):
    empresa = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    tipo = models.CharField(max_length=100,choices=Tipo.choices,default=Tipo.Outros)
    plano = models.CharField(max_length=100,choices=Plan_status.choices,default=Plan_status.SIMPLES)
    telefone = models.CharField(max_length=15, unique=True)
    data_adesão = models.DateTimeField(auto_now_add=True, editable=False)
    imagem = models.BinaryField(null=True, blank=True)

    
    def __str__(self):
        return self.model_name

# Classe de configurações do modelo
class Usuarios(models.Model):
    user= models.AutoField(primary_key=True)
    empresa_id = models.ForeignKey(Empresas, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=11)
    nome = models.CharField(max_length=255)
    cargo = models.CharField(max_length=255)
    email = models.EmailField()
    telefone = models.CharField(max_length=15,unique=True)
    tipo = models.CharField(max_length=100,choices=Tipo_usuario,default=Tipo_usuario.VIEW)
    primeiro_acesso = models.DateTimeField(auto_now_add=True,editable=False)
    ultimo_acesso = models.DateTimeField(auto_now_add=True)
    imagem = models.BinaryField(null=True,blank=True)
    password = models.CharField(max_length=128)
        
    def __str__(self):
        return self.model_name
