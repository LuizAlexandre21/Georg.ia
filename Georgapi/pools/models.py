from django.db import models

# Classe de configurações do modelos 
class LLM_Config(models.Model):
    model_name = models.CharField(max_length=255)
    model_url = models.CharField()
    temperature = models.FloatField(default=0.7)
    max_tokens = models.IntegerField(default=512)

    def __str__(self):
        return self.model_name

# Classe de interação do modelo
class LLM_Request(models.Model):
    session_id = models.CharField(max_length=255,unique=True)
    user_id = models.IntegerField()
    pergunta = models.TextField()
    resposta = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Request {self.id} - {self.created_at}"
    

class LLM_Session(models.Model):
    session_id = models.CharField(max_length=255, unique=True)
    user_id = models.IntegerField()
    model_config = models.ForeignKey(LLM_Config, on_delete=models.SET_NULL, null=True, blank=True)  # Configuração do modelo utilizado
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)  # Pode ser null se a sessão ainda estiver ativa
    is_active = models.BooleanField(default=True)  # Status se a sessão está ativa ou não

    def __str__(self):
        return f"Session {self.session_id} - User {self.user_id}"

class LLM_Interaction_Log(models.Model):
    session_id = models.ForeignKey(LLM_Session, on_delete=models.CASCADE)  # Sessão associada
    user_id = models.IntegerField()
    request = models.TextField()  # A pergunta enviada pelo usuário
    response = models.TextField()  # A resposta gerada pelo modelo
    timestamp = models.DateTimeField(auto_now_add=True)
    request_type = models.CharField(max_length=50, choices=[('text', 'Text'), ('voice', 'Voice')], default='text')  # Tipo de requisição (ex: texto ou voz)

    def __str__(self):
        return f"Log {self.id} - Session {self.session_id} - {self.timestamp}"
    
