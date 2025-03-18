from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from pools.accounts.models import Empresas,Usuarios
from pools.accounts.serializers import EmpresaSerializer,UsuarioSerializer,LoginSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated


# Criando o View set para a Empresa 
class EmpresaView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self,request):
        empresas = Empresas.objects.all()
        serializer = EmpresaSerializer(empresas,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serialzer =EmpresaSerializer(data=request.data)
        if serialzer.is_valid():
            serialzer.save()
            return Response(serialzer.data,status=status.HTTP_201_CREATED)
        return Response(serialzer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request,pk):
        usuarios = get_object_or_404(Usuarios,pk=pk)
        serializer = UsuarioSerializer(usuarios,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        usuarios = get_object_or_404(Usuarios,pk=pk)
        usuarios.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# Criando o View set para os Usuarios 
class UsuarioView(APIView):

    def get(self,request):
        usuarios = Usuarios.objects.all()
        serializer = UsuarioSerializer(usuarios,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        usuarios = get_object_or_404(Usuarios,pk=pk)
        serializer = UsuarioSerializer(usuarios,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        usuario = get_object_or_404(Usuarios,pk=pk)
        usuario.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


