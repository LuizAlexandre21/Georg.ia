from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.conf import settings
from pools.accounts.utils import PlanStatus,Tipo,TipoUsuario,UsuarioManager

# Criando o modelos de empresas 
class Empresas(models.Model):
    empresa = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    tipo = models.CharField(max_length=100,choices=Tipo.choices,default=Tipo.OUTROS)
    plano = models.CharField(max_length=100,choices=PlanStatus.choices,default=PlanStatus.SIMPLES)
    telefone = models.CharField(max_length=15, unique=True)
    data_adesão = models.DateTimeField(auto_now_add=True, editable=False)
    imagem = models.BinaryField(null=True, blank=True)


# Classe de configurações do modelo

class Usuarios(AbstractBaseUser, PermissionsMixin):
    user = models.AutoField(primary_key=True)
    empresa = models.ForeignKey(Empresas, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=11)
    nome = models.CharField(max_length=255)
    cargo = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=15, unique=True)
    tipo = models.CharField(max_length=100, choices=TipoUsuario, default=TipoUsuario.VIEW)
    primeiro_acesso = models.DateTimeField(auto_now_add=True, editable=False)
    ultimo_acesso = models.DateTimeField(auto_now_add=True)
    imagem = models.BinaryField(null=True, blank=True)

    is_active = models.BooleanField(default=True)  # 🔥 Necessário para autenticação
    is_staff = models.BooleanField(default=False)  # 🔥 Necessário para permissões

    objects = UsuarioManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.email