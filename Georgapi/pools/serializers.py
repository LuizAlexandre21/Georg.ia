# Bibliotecas 
from rest_framework import serializers
from .models import config_model, config_session, chat_model 

class ConfigModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = config_model 
        fields = ['empresa','modelo', 'url_modelo', 'temperatura', 'num_tokens', 'prompt','tabelas','schema','db_uri']


class ConfigSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = config_session
        fields = ['nome','is_active','user','config']


class ChatModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = chat_model
        fields =['session','question','answer']


