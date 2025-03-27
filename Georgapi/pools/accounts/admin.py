from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token

from .serializers import UsuarioSerializer,LoginSerializer

# View para Registro 
class RegisterView(APIView):
     permission_classes = [AllowAny]
     def post(self, request):
        # Ao criar um novo usuário, a senha precisa ser passada de forma segura
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            # O `save()` já vai cuidar de salvar a senha corretamente (com hash)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
# View para o Login
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data,status=status.HTTP_200_OK)


# View para o Logout 
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        try: 
            refresh_token = request.data['refresh']
            token = refresh_token(refresh_token)
            token.blacklist()
        
            return Response({"detail": "Logout realizado com sucesso."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Token inválido ou já expirado."}, status=status.HTTP_400_BAD_REQUEST)
