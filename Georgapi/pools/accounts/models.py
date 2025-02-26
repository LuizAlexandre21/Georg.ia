from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.conf import settings

# Criando o gerenciador de usuários
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O email é obrigatório")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)


class User_Info(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    username = models.CharField(unique=True,max_length=255, blank=True, null=True) 
    email = models.EmailField(unique=False)  # E-mail único
    first_name = models.CharField(max_length=255, blank=True, null=True)  # Nome (opcional)
    last_name = models.CharField(max_length=255, blank=True, null=True)  # Sobrenome (opcional)
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Número de telefone (opcional)
    address = models.TextField(blank=True, null=True)  # Endereço (opcional)
    date_of_birth = models.DateField(null=True, blank=True)  # Data de nascimento (opcional)
    created_at = models.DateTimeField(default=timezone.now)  # Data de criação do usuário
    updated_at = models.DateTimeField(auto_now=True)  # Data da última atualização
    
    # Campos necessários para autenticação
    last_login = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)  # Indica se o usuário está ativo
    is_staff = models.BooleanField(default=False)  # Indica se o usuário tem permissão de acesso ao admin
    is_superuser = models.BooleanField(default=False)  # Indica se o usuário é superusuário
    
    USERNAME_FIELD = 'username'  # Campo para autenticação
    REQUIRED_FIELDS = ['username']  # Campos obrigatórios para criação do usuário
    
    objects = UserManager()  # Definindo o gerenciador de usuários customizado

    def __str__(self):
        return self.username  # Corrigido para retornar o username

