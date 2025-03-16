from django.db import models

class Plan_status(models.TextChoices):
    SIMPLES = 'simples','Simples','SIMPLES'
    AVANÇADO = 'avançado','Avançado','AVANÇADO'
    COMPLETO = 'completo','Completo','COMPLETO'


class Tipo (models.TextChoices):
    PREFEITURAS = 'prefeituras','Prefeituras','PREFEITURAS'
    ESTADO = 'estado','Estado','ESTADO'
    FEDERAL = 'federal','Federal','FEDERAL'
    ONG = 'ong','Ong','ONG'
    Outros = 'outros','Outros','OUTROS'


class Tipo_usuario(models.TextChoices):
    VIEW = 'view','View','VIEW'
    EDIT = 'edit','Edit','EDIT'
    ADMIN = 'admin','Admin','ADMIN'
    OWNER = 'owner','Owner','OWNER'
