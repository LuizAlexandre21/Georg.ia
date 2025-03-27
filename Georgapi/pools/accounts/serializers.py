from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Empresas,Usuarios
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresas
        fields =['nome','tipo','plano','telefone','imagem']


class UsuarioSerializer(serializers.ModelSerializer):
    
    #empresa_id = serializers.PrimaryKeyRelatedField(queryset=Empresas.objects.all())  # Refere-se à empresa pelo ID
    empresa_id = serializers.IntegerField()
    password = serializers.CharField(write_only=True)  # Não exibe a senha na resposta
    class Meta:
        model = Usuarios
        fields = ['empresa_id','cpf','nome','cargo','email','telefone','tipo','imagem','password']
        read_only_fields = ['empresa_id','primeiro_acesso','ultimo_acesso']
    
    def create(self, validated_data):
        # Antes de salvar o usuário, vamos encriptar a senha
        password = validated_data.pop('password')  # Remove a senha do validated_data
        usuario = Usuarios(**validated_data)  # Cria o objeto usuário sem a senha
        usuario.password = make_password(password)  # Encripta a senha antes de salvar
        usuario.save()  # Salva o usuário no banco de dados
        return usuario

    
class LoginSerializer(serializers.Serializer):
    cpf = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        cpf = attrs.get("cpf")
        password = attrs.get("password")

        if not cpf or not password:
            raise AuthenticationFailed("CPF and password are required")
        
        try:
            user = Usuarios.objects.get(cpf=cpf)
        except Usuarios.DoesNotExist:
            raise AuthenticationFailed("User with this CPF does not exist")

        # Autentica o usuário com cpf e senha
        user = authenticate(cpf=cpf, password=password)

        if not user:
            raise AuthenticationFailed("Invalid credentials")
        
        # Gerar tokens (usando o campo CPF, pois o modelo não possui o campo 'id')
        refresh = RefreshToken.for_user(user)

        return {
            "user_id": user.cpf,  # Usando o CPF como identificador
            "cpf": user.cpf,  # Aqui você mantém o CPF
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }