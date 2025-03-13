from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from django.contrib.auth import authenticate
from .models import User_Info
from .serializers import UserSerializer
from django.contrib.auth.models import User  # Importando o modelo User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

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
            email=validated_data.get("email"),
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

    def post(self, request, *args, **kwargs):
        """
        Recebe username e senha, autentica o usuário e retorna um token.
        """
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username e senha são obrigatórios"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Credenciais inválidas"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    """
    API para logout de um usuário autenticado (revoga o token).
    """
    authentication_classes = [TokenAuthentication]  # 🔥 Necessário para autenticar via token
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Apaga o token do usuário.
        """
        request.user.auth_token.delete()
        return Response({"message": "Logout realizado com sucesso"}, status=status.HTTP_200_OK)
    

class DeleteUserView(APIView):
    """
    API para deletar a conta do usuário autenticado.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        """
        Deleta o usuário autenticado.
        """
        user = request.user
        user.delete()
        return Response({"message": "Usuário deletado com sucesso"}, status=status.HTTP_200_OK)