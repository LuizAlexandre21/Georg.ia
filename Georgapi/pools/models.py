from django.db import models
from django.utils import timezone
from pools.accounts.models import User_Info


# Classe de configurações do modelo
class LLM_Config(models.Model):
    model_name = models.CharField(max_length=255)
    model_url = models.CharField(max_length=255)  # Adicionado o max_length
    temperature = models.FloatField(default=0.7)
    max_tokens = models.IntegerField(default=512)
    prompt = models.TextField(default='', null=True, blank=True)
    session = models.ForeignKey('LLM_Session', on_delete=models.SET_NULL, null=True, blank=True, related_name="configurations")

    def __str__(self):
        return self.model_name


# Classe para gerenciar sessões do modelo
class LLM_Session(models.Model):
    session = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User_Info, on_delete=models.CASCADE, related_name="sessions")  # Relacionado com o usuário
    model_config = models.ForeignKey(LLM_Config, on_delete=models.SET_NULL, null=True, blank=True, related_name="sessions")  # Configuração do modelo
    started_at = models.DateTimeField(default=timezone.now)  # Definindo a data de início
    name_model = models.CharField(max_length=255, null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)  # Pode ser null se a sessão ainda estiver ativa
    is_active = models.BooleanField(default=True)  # Status se a sessão está ativa ou não

    def __str__(self):
        return f"Session {self.session} - User {self.user.username}"

# Classe de interação do modelo
class LLM_Request(models.Model):
    session = models.ForeignKey(LLM_Session, on_delete=models.CASCADE, related_name="requests")  # Relacionado com a sessão
    user = models.ForeignKey(User_Info, on_delete=models.CASCADE, related_name="requests")  # Relacionado com o usuário
    pergunta = models.TextField()
    resposta = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)  # Definindo a data de criação
    update_date = models.DateTimeField(auto_now=True)  # Atualização automática

    def __str__(self):
        return f"Request {self.id} - {self.create_date}"

# Log de interações com o modelo
class LLM_Interaction_Log(models.Model):
    session = models.ForeignKey(LLM_Session, on_delete=models.CASCADE, related_name="logs")
    user = models.ForeignKey(User_Info, on_delete=models.CASCADE, null=True, related_name="logs")  # Permite null
    request = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    request_type = models.CharField(max_length=50, choices=[('text', 'Text'), ('voice', 'Voice')], default='text')

    def __str__(self):
        return f"Log {self.id} - Session {self.session.session} - {self.timestamp}"
