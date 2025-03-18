from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from .models import Usuarios
from .serializers import UsuarioSerializer, LoginSerializer

# View para CRUD de usuários
class UsuarioView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        usuarios = Usuarios.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(user.password)  # Criptografa a senha
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        usuario = get_object_or_404(Usuarios, pk=pk)
        serializer = UsuarioSerializer(usuario, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        usuario = get_object_or_404(Usuarios, pk=pk)
        usuario.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# View para registro de usuário (sem necessidade de autenticação)
class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(user.password)  # Criptografa a senha
            user.save()
            token, _ = Token.objects.get_or_create(user=user)  # Gera um token para o usuário
            return Response({"user": serializer.data, "token": token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# View para login de usuário
class LoginViewSet(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            user = authenticate(email=email, password=password)
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({"token": token.key}, status=status.HTTP_200_OK)
            return Response({"error": "Credenciais inválidas"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# View para logout de usuário autenticado
class LogoutViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()  # Revoga o token
        return Response({"message": "Logout realizado com sucesso"}, status=status.HTTP_200_OK)
