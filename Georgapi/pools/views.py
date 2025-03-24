from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status 
from django.shortcuts import get_object_or_404
from pools.models import config_model,chat_model,config_session
from pools.serializers import ChatModelSerializer,ConfigSessionSerializer,ConfigModelSerializer 
from rest_framework.permissions import IsAuthenticated
from src.georg.model.langchain_database import LLMdatabase 
from src.georg.graph.graph import TextProcessingGraph 
from django.forms.models import model_to_dict

# Criando o View set para as configurações do modelo 
class ConfigmodelView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        config = config_model.objects.all()
        serializer = ConfigModelSerializer(config,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = ConfigModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

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
        serializer = ConfigSessionSerializer(data=request.data)
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

        config_model = model_to_dict(config_model.objects.get(empresa=request.user.empresa))
        config = {key:elem for key,elem in config_model.items() if key not in ['config','empresa']} 


        graph = TextProcessingGraph(LLMdatabase(config))
        result = graph.run(request.data['question'])

        dados = request.data.copy() 
        dados["answer"] = result['llm_response']

        serializer = ChatModelSerializer(data=dados)
        if serializer.is_valid():
            
            serializer.save()

            return Response(
                {"llm_response": result['llm_response']},
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
