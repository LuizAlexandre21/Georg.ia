from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from .views import ConfigmodelView, ConfigSessionView, ChatModelView

# Definindo a visualização da documentação da API
schema_view = get_schema_view(
   openapi.Info(
      title="Georg.ia - LLM Gestão Eficiente de Orçamentos e Recursos Governamentais com IA",
      default_version='v1',
      description="Documentação da API para o projeto de LLM Gestão Eficiente de Orçamentos e Recursos Governamentais com Inteligência Artificial",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="luizalexandre21@outlook.com"),
      license=openapi.License(name="Licença MIT"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

# URLs para as configurações do modelo
urlpatterns = [
    path('config-model/', ConfigmodelView.as_view(), name='config-model-list'),  # GET e POST para listar e criar configurações do modelo
    path('config-model/<int:pk>/', ConfigmodelView.as_view(), name='config-model-detail'),  # GET, PUT e DELETE para detalhes e manipulação de configuração do modelo

    # URLs para as configurações da sessão
    path('config-session/', ConfigSessionView.as_view(), name='config-session-list'),  # GET e POST para listar e criar configurações de sessão
    path('config-session/<int:pk>/', ConfigSessionView.as_view(), name='config-session-detail'),  # GET, PUT e DELETE para detalhes e manipulação de configuração da sessão

    # URLs para o modelo de chat
    path('chat-model/', ChatModelView.as_view(), name='chat-model-list'),  # GET e POST para listar e criar entradas no modelo de chat
    path('chat-model/<int:pk>/', ChatModelView.as_view(), name='chat-model-detail'),  # GET, PUT e DELETE para detalhes e manipulação de entradas no modelo de chat
    
    # Swagger UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # Acessar Swagger UI
]
