from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status 
from django.shortcuts import get_object_or_404
from pools.models import config_model,chat_model,config_session
from pools.serializers import ChatModelSerializer,ConfigSessionSerializer,ConfigModelSerializer 
from rest_framework.permissions import IsAuthenticated
from src.georg.model.langchain_database import LLMdatabase 
from src.georg.graph.graph import TextProcessingGraph 

# Criando o View set para as configurações do modelo 
class ConfigmodelView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        config = config_model.objects.all()
        serializer = ConfigModelSerializer(config,many=True)
        return Response(serializer.data)
    
    def put(self,request,pk):
        config = get_object_or_404(config_model,pk=pk)
        serializer = ConfigModelSerializer(config,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class ConfigSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,requets):
        config = config_session.objects.all()
        serializer = ConfigSessionSerializer(config,many=True)
        return Response(serializer.data)

    def post(self,request): 
        serializer = ConfigSessionSerializer(data=request)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request,pk):
        config = get_object_or_404(config_session,pk=pk)
        serializer = ConfigSessionSerializer(config,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        config = get_object_or_404(config_session,pk=pk)
        config.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
#TODO: Revisar esse endpoint aqui 
class ChatModelView(APIView):
    permission_classes =[IsAuthenticated]
    

    def get(self,requests):
        chat = chat_model.objects.all()
        serializer = ChatModelSerializer(chat,many=True)
        return Response(serializer.data)

    def post(self,request):
        config = config_model.objects.filter(empresa=request.user.empresa)
        serializer = ChatModelSerializer(data=request)
        if serializer.is_valid():
            llm_model = LLMdatabase(config)
            graph = TextProcessingGraph(llm_model)
            result = graph.run(serializer.validated_data['pergunta'])

            llm_request = serializer.save(resposta=result.get("llm_response"))

            return Response(
                {"request_id": llm_request.id, "llm_response": result.get("llm_response")},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self,request,pk):
        chat = get_object_or_404(config_session,pk=pk)
        serializer = ChatModelSerializer(chat,data=request,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        chat = get_object_or_404(chat,pk=pk)
        chat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
