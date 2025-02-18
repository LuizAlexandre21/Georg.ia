from django.db import models
from django.utils import timezone

# Classe de configurações do modelo
class LLM_Config(models.Model):
    model_name = models.CharField(max_length=255)
    model_url = models.CharField(max_length=255)  # Adicionado o max_length
    temperature = models.FloatField(default=0.7)
    max_tokens = models.IntegerField(default=512)
    prompt = models.TextField(default='',null=True)
    session_id = models.ForeignKey('LLM_Session', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.model_name

# Classe de interação do modelo
class LLM_Request(models.Model):
    session = models.ForeignKey('LLM_Session', on_delete=models.CASCADE)  # Relacionado com a sessão
    user = models.ForeignKey('User_Info', on_delete=models.CASCADE)  # Relacionado com o usuário
    pergunta = models.TextField()
    resposta = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)  # Definindo a data de criação
    update_date = models.DateTimeField(auto_now=True)  # Atualização automática

    def __str__(self):
        return f"Request {self.id} - {self.create_date}"

# Classe para gerenciar sessões do modelo
class LLM_Session(models.Model):
    session = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey('User_Info', on_delete=models.CASCADE)  # Relacionado com o usuário
    model_config = models.ForeignKey(LLM_Config, on_delete=models.SET_NULL, null=True, blank=True)  # Configuração do modelo utilizado
    started_at = models.DateTimeField(default=timezone.now)  # Definindo a data de início
    name_model = models.CharField(max_length=255,null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)  # Pode ser null se a sessão ainda estiver ativa
    is_active = models.BooleanField(default=True)  # Status se a sessão está ativa ou não

    def __str__(self):
        return f"Session {self.session_id} - User {self.user.username}"

# Log de interações com o modelo
class LLM_Interaction_Log(models.Model):
    session = models.ForeignKey(LLM_Session, on_delete=models.CASCADE)
    user = models.ForeignKey('User_Info', on_delete=models.CASCADE, null=True)  # Permite null
    request = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    request_type = models.CharField(max_length=50, choices=[('text', 'Text'), ('voice', 'Voice')], default='text')

    def __str__(self):
        return f"Log {self.id} - Session {self.session.session} - {self.timestamp}"



# Classe para armazenar informações do usuário
class User_Info(models.Model):
    user = models.AutoField(primary_key=True)  # Chave primária automática
    username = models.CharField(max_length=255, unique=True)  # Nome de usuário único
    email = models.EmailField(unique=True)  # E-mail único
    first_name = models.CharField(max_length=255, blank=True, null=True)  # Nome (opcional)
    last_name = models.CharField(max_length=255, blank=True, null=True)  # Sobrenome (opcional)
    password = models.CharField(max_length=255)  # Senha do usuário (recomendação: utilizar hash em vez de texto simples)
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Número de telefone (opcional)
    address = models.TextField(blank=True, null=True)  # Endereço (opcional)
    date_of_birth = models.DateField(null=True, blank=True)  # Data de nascimento (opcional)
    created_at = models.DateTimeField(default=timezone.now)  # Data de criação do usuário
    updated_at = models.DateTimeField(auto_now=True)  # Data da última atualização

    def __str__(self):
        return self.username  # Retorna o nome de usuário ao exibir o modelo

    class Meta:
        verbose_name = 'User Info'
        verbose_name_plural = 'User Infos'
