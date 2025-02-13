# Bibliotecas 
from rest_framework import serializers
from .models import LLM_Config,LLM_Request,LLM_Interaction_Log,LLM_Session

class LLMRequestSerializerpost(serializers.ModelSerializer):
    class Meta:
        model = LLM_Request
        fields = ('session_id','user_id','pergunta')


class LLMRequestSerializerget(serializers.ModelSerializer):
    class Meta:
        model = LLM_Request
        fields = '__all__'

        
class LLMConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = LLM_Config
        fields = '__all__'
class UsageLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = LLM_Interaction_Log
        fields = '__all__'


class LLMSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LLM_Session
        fields = '__all__'

