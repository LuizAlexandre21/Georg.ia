from rest_framework import viewsets,permissions,status 
from rest_framework.response import Response 
from rest_framework.authtoken.models import Token 
from rest_framework.views import APIView 
from rest_framework.generics import CreateAPIView
from django.contrib.auth import authenticate
from .models import User_Info 
from .serializers import UserSerializer

# Crud de usuarios 
class UserViewSet(viewsets.ModelViewSet):

    queryset = User_Info.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self,serializer):

        user = serializer.save()
        user.set_password(user.password)
        user.save()

# Registro de usuarios 
class RegisterUserView(CreateAPIView):
    queryset = User_Info.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    # Adicionando a criptografia da senha
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.set_password(user.password)
        user.save()

        # Criando uk token 
        token,created = token.object.get_or_create(user=user)

        return Response({
            "user":UserSerializer(user).data,
            "token":token.key
        },status=status.HTTP_201_CREATED)


# Login e Geração de token
class LoginView(APIView):
    
    permission_classes = [permissions.AllowAny]
    
    def post(self,request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email,password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token":token.key},status=status.HTTP_200_OK)
        else:
            return Response({"error": "Credenciais inválidas"}, status=status.HTTP_401_UNAUTHORIZED)


# Logout 
class LogoutView(APIView):
    """
    API para logout de um usuário autenticado (revoga o token).
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Apaga o token do usuário.
        """
        request.user.auth_token.delete()
        return Response({"message": "Logout realizado com sucesso"}, status=status.HTTP_200_OK)
