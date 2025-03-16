from rest_framework import serializers
from .models import Empresas,Usuarios
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token

class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresas
        fields =['nome','tipo','plano','telefone','imagem']


class UsuarioSerializer(serializers.ModelSerializer):
    empresa_id = serializers.PrimaryKeyRelatedField(queryset=Empresas.objects.all())  # Refere-se à empresa pelo ID
    password = serializers.CharField(write_only=True)  # Não exibe a senha na resposta
    class Meta:
        model = Usuarios
        fields = ['empresa_id','cpf','nome','cargo','email','telefone','tipo','imagem','password']
        read_only_fields = ['empresa_id','primeiro_acesso','ultimo_acesso']

    def create(self,validated_data):
        password = validated_data.pop("password")
        usuario=Usuarios(**validated_data)
        usuario.set_password(password)
        usuario.save()
        return usuario
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self,attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        user = authenticate(username=username,password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials')
        
        token,created = Token.objects.get_or_create(user=user)

        return {"token":token.key}