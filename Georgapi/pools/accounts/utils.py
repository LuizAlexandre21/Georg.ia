from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class PlanStatus(models.TextChoices):
    SIMPLES = 'simples', 'Simples'
    AVANCADO = 'avancado', 'Avançado'
    COMPLETO = 'completo', 'Completo'

class Tipo(models.TextChoices):
    PREFEITURA = 'prefeitura', 'Prefeitura'
    ESTADO = 'estado', 'Estado'
    FEDERAL = 'federal', 'Federal'
    ONG = 'ong', 'Ong'
    OUTROS = 'outros', 'Outros'

class TipoUsuario(models.TextChoices):
    VIEW = 'view', 'View'
    EDIT = 'edit', 'Edit'
    ADMIN = 'admin', 'Admin'
    OWNER = 'owner', 'Owner'


class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O e-mail é obrigatório")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # 🔥 Usa set_password para criptografar a senha
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)
    
    
