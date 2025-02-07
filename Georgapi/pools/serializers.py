# Bibliotecas 
from rest_framework import serializers
from .models import LLMRequest, LLMConfig,ChatSession,ChatMessage,UsageLog

class LLMRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LLMRequest
        fields = '__all__'

class LLMConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = LLMConfig
        fields = '__all__'
        
class ChatSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatSession
        fields = '__all__'

class ChatMessageSerializer(serializers.ModelSerializer):
    session = serializers.PrimaryKeyRelatedField(queryset=ChatSession.objects.all())

    class Meta:
        model = ChatMessage
        fields = '__all__'

class UsageLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsageLog
        fields = '__all__'