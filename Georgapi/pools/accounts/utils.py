from django.db import models

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
