from django.db import models
from django.utils import timezone
from pools.accounts.models import Empresas,Usuarios
from django.db.models.signals import pre_save
from django.dispatch import receiver


# Modelo de Configuração do agente 
class config_model(models.Model):
    config = models.AutoField(primary_key=True)
    empresa = models.ForeignKey(Empresas,on_delete=models.CASCADE)
    modelo = models.CharField(max_length=255)
    url_modelo = models.CharField(max_length=255)
    temperatura = models.FloatField()
    num_tokens = models.IntegerField()
    prompt = models.TextField()


# Modelo de Configuração de sessões 
class config_session(models.Model):
    session = models.AutoField(primary_key=True)
    user = models.ForeignKey(Usuarios,on_delete=models.CASCADE)
    nome = models.CharField(max_length=255)
    is_active = models.BooleanField()
    id_config = models.ForeignKey(config_model,on_delete=models.CASCADE)


# Modelo de Conversa 
class chat_model(models.Model):
    chat = models.AutoField(primary_key=True)
    session = models.ForeignKey(config_session,on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)  # Definindo a data de criação


@receiver(pre_save,sender=Usuarios)
def trigger_modelconfig(sender,instance,**kwarg):
    if not config_model.objects.filter(id=instance.categoria_id).exists():
        config_model.objects.get_or_create(user=instance.user,defaults={
            'nome':'llama3',
            'url_modelo':'https://www.llama.com',
            'temperatura':'0.1',
            'tokens':'100',
            'prompt':'',
        })