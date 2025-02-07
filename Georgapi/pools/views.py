from django.shortcuts import render
from django.http import HttpResponse 
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status 
from src.georg.graph.graph import TextProcessingGraph 
from src.georg.model.langchain_database import LLMdatabase 
from .models import LLMRequest,LLMConfig,ChatMessage,ChatSession,UsageLog 
from .serializers import (
    LLMRequestSerializer,
    LLMConfigSerializer,
    ChatSessionSerializer,
    ChatMessageSerializer,
    UsageLogSerializer,
)

# Create your views here.
class LLMRequestViewSet(viewsets.ModelViewSet):
    queryset = LLMRequest.objects.all().order_by('-created_at')
    serializer_class = LLMRequestSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            llm_request = serializer.save()
            
            # Inicializa o modelo de LLM e o grafo
            llm_model = LLMdatabase()
            graph = TextProcessingGraph(llm_model)
            
            # Executa o grafo com o texto da requisição
            result = graph.run(llm_request.input_text)  # Certifique-se de que o modelo tem essa coluna
            
            return Response(
                {"request_id": llm_request.id, "llm_response": result.get("llm_response")},
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LLMConfigViewSet(viewsets.ModelViewSet):
    queryset = LLMConfig.objects.all()
    serializer_class = LLMConfigSerializer

class ChatSessionViewSet(viewsets.ModelViewSet):
    queryset = ChatSession.objects.all().order_by('-created_at')
    serializer_class = ChatSessionSerializer


class ChatMessageViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.all().order_by('-created_at')
    serializer_class = ChatMessageSerializer


class UsageLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UsageLog.objects.all().order_by('-timestamp')
    serializer_class = UsageLogSerializer