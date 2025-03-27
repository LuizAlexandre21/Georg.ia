from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from pools.accounts.models import Empresas,Usuarios
from pools.accounts.serializers import EmpresaSerializer,UsuarioSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated


# Criando o View set para a Empresa 
class EmpresaView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self,request,pk=None):
        if pk == None:
            empresas = Empresas.objects.all()
            serializer = EmpresaSerializer(empresas,many=True)
            return Response(serializer.data)
        else:
            try:
                emp = Empresas.objects.get(empresa=pk)
                serializer = EmpresaSerializer(emp)
                return Response(serializer.data)
            except:
                return Response({'error': 'Empresa não encontrada'}, status=status.HTTP_404_NOT_FOUND)

    
    def post(self,request):
        serialzer =EmpresaSerializer(data=request.data)
        if serialzer.is_valid():
            serialzer.save()
            return Response(serialzer.data,status=status.HTTP_201_CREATED)
        return Response(serialzer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request,pk):
        empresas = get_object_or_404(Empresas,pk=pk)
        serializer = EmpresaSerializer(empresas,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        empresas = get_object_or_404(Empresas,pk=pk)
        empresas.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Criando o View set para os Usuarios 

class UsuarioView(APIView):
    permission_classes = [IsAuthenticated] 
    
    def get(self,request,pk=None):
        if pk == None:
            usuarios = Usuarios.objects.all()
            serializer = UsuarioSerializer(usuarios,many=True)
            return Response(serializer.data)
        else:
            try:
                emp = Usuarios.objects.get(user=pk)
                serializer = UsuarioSerializer(emp)
                return Response(serializer.data)
            except:
                return Response({'error': 'Usuario não encontrada'}, status=status.HTTP_404_NOT_FOUND)

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


