from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from django.contrib.auth import authenticate
from .models import User_Info
from .serializers import UserSerializer
from django.contrib.auth.models import User  # Importando o modelo User

# 📌 1. ViewSet para CRUD de Usuários
class UserViewSet(viewsets.ModelViewSet):
    """
    API para gerenciar usuários (listar, criar, atualizar e deletar).
    Apenas usuários autenticados podem acessar.
    """
    queryset = User_Info.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer,*args,**kwargs):
        """
        Sobrescreve a criação para garantir que a senha seja salva corretamente.
        """
        user = serializer.save()
        user.set_password(user.password)  # Criptografa a senha
        user.save()


# 📌 2. View para Registro de Usuários
class RegisterUserView(CreateAPIView):
    """
    API para criar um novo usuário.
    Qualquer pessoa pode se registrar.
    """
    queryset = User_Info.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        """
        Sobrescreve a criação para garantir a criptografia da senha.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Obtém os dados validados
        validated_data = serializer.validated_data

        # Criando o usuário corretamente usando o User do Django
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
        )

        # Criando o objeto User_Info associando o usuário
        user_info = User_Info.objects.create(user=user)

        # Gera um token para o usuário registrado
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "user": UserSerializer(user).data,
            "token": token.key
        }, status=status.HTTP_201_CREATED)


# 📌 3. View para Login e Geração de Token
class LoginView(APIView):
    """
    API para autenticar um usuário e gerar um token.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request,*args,**kwargs):
        """
        Recebe email e senha, autentica o usuário e retorna um token.
        """
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Credenciais inválidas"}, status=status.HTTP_401_UNAUTHORIZED)


# 📌 4. View para Logout (Revogar Token)
class LogoutView(APIView):
    """
    API para logout de um usuário autenticado (revoga o token).
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request,*args,**kwargs):
        """
        Apaga o token do usuário.
        """
        request.user.auth_token.delete()
        return Response({"message": "Logout realizado com sucesso"}, status=status.HTTP_200_OK)
