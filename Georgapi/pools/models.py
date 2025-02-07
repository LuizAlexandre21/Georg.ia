from django.db import models

# Create your models here.

class LLMRequest(models.Model):

    user_input = models.TextField()
    model_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    base_url = models.DateTimeField()

    def __str__(self):
        return f"Request {self.id} - {self.created_at}"

class LLMConfig(models.Model):

    model_name = models.CharField(max_length=255)
    temperature = models.FloatField(default=0.7)
    max_tokens = models.IntegerField(default=512)

    def __str__(self):
        return self.model_name
    

class ChatSession(models.Model):
    session_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Session {self.session_id}"
    

class ChatMessage(models.Model):

    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=[('user','User'),('assistant', 'Assistant')])
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role} - {self.created_at}"
    
class UsageLog(models.Model):

    timestamp = models.DateTimeField(auto_now_add=True)
    model_name = models.CharField(max_length=255)
    request_tokens = models.IntegerField()
    response_tokens = models.IntegerField()
    total_cost = models.FloatField()

    def __str__(self):
        return f"Log {self.id} - {self.model_name}"
    
