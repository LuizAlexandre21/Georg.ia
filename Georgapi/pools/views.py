from django.shortcuts import render
from django.http import JsonResponse 
from rest_framework import viewsets
import json
from rest_framework.response import Response
from rest_framework import status 
from src.georg.graph.graph import TextProcessingGraph 
from src.georg.model.langchain_database import LLMdatabase 
from .models import *
from .serializers import UsageLogSerializer, LLMConfigSerializer, LLMRequestSerializer,LLMSessionSerializer

# Create your views here.
class LLMRequestViewSet(viewsets.ModelViewSet):
    queryset = LLM_Request.objects.all()
    serializer_class = LLMRequestSerializer


    def create(self,request,*args,**kwargs):
        serializer =self.get_serializer(data=request.data)
        if serializer.is_valid():
    
            llm_model = LLMdatabase()
            graph = TextProcessingGraph(llm_model)

            result = graph,run(llm_request.input_text)

            llm_request = serializer.save(resposta = result.get("llm_response"))

            return Response(
                {"request_id": llm_request.id, "llm_response": result.get("llm_response")},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, *args, **kwargs):

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        
        instance = self.get_object()
        serializer = self.get_serializer(instance,data=request.data)
        if serializer.is_valid():
            # Se válido, atualiza a instância com os novos dados
            llm_model = LLMdatabase()
            graph = TextProcessingGraph(llm_model)
            result = graph.run(serializer.validated_data['input_text'])
            
            # Atualiza a resposta do modelo com a nova informação
            llm_request = serializer.save(resposta=result.get("llm_response"))

            return Response(
                {"request_id": llm_request.id, "llm_response": result.get("llm_response")},
                status=status.HTTP_200_OK
            )
        
        # Caso os dados não sejam válidos, retorna os erros de validação
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LLMConfigViewSet(viewsets.ModelViewSet):
    queryset = LLM_Config.objects.all()
    serializer_class = LLMConfigSerializer

    def create(self,request,*args,**kwargs):
        serializer =self.get_serializer(data=request.data)
       
        if serializer.is_valid():
           
            llm_config = serializer.save()
            return Response({'id':llm_config.id,"model_name":llm_config.model_name},status = status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, *args, **kwargs):
        
        instance = self.get_object()

        serializer = self.get_serializer(instance)

        return Response(serializer.data)
    

class LLMSessionViewSet(viewsets.ModelViewSet):
    queryset = LLM_Session.objects.all()
    serializer_class = LLMSessionSerializer

    def create(self, request, *args, **kwargs):
        """
        Método POST para criar uma nova sessão LLM.
        """
        # Criação do serializer com os dados enviados na requisição
        serializer = self.get_serializer(data=request.data)
        
        # Verifica se os dados são válidos
        if serializer.is_valid():
            # Salva a nova sessão LLM no banco de dados
            llm_session = serializer.save()
            
            # Retorna a resposta com a sessão criada
            return Response(
                {"session_id": llm_session.session_id, "user_id": llm_session.user_id},
                status=status.HTTP_201_CREATED
            )
        
        # Se os dados não forem válidos, retorna os erros de validação
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        """
        Método GET para recuperar uma sessão LLM específica.
        """
        # Recupera a instância de LLM_Session com base no ID da URL
        instance = self.get_object()
        
        # Serializa a instância para o formato JSON
        serializer = self.get_serializer(instance)
        
        # Retorna a resposta com os dados da sessão
        return Response(serializer.data)


class LLMRequestViewSet(viewsets.ModelViewSet):
    queryset = UsageLogSerializer.objects.all()
    serializer_class = UsageLogSerializer

    def create(self, request, *args, **kwargs):
        """
        Método POST para criar uma nova requisição LLM.
        """
        # Criação do serializer com os dados enviados na requisição
        serializer = self.get_serializer(data=request.data)
        
        # Verifica se os dados são válidos
        if serializer.is_valid():
            # Salva a nova requisição LLM no banco de dados
            llm_request = serializer.save()
            
            # Retorna a resposta com a requisição criada
            return Response(
                {"request_id": llm_request.id, "user_id": llm_request.user_id},
                status=status.HTTP_201_CREATED
            )
        
        # Se os dados não forem válidos, retorna os erros de validação
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        """
        Método GET para recuperar uma requisição LLM específica.
        """
        # Recupera a instância de LLM_Request com base no ID da URL
        instance = self.get_object()
        
        # Serializa a instância para o formato JSON
        serializer = self.get_serializer(instance)
        
        # Retorna a resposta com os dados da requisição
        return Response(serializer.data)
