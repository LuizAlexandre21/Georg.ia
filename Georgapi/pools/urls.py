from django.urls import path,include 
from rest_framework.routers import DefaultRouter
from .views import (
    LLMRequestViewSet,
    LLMConfigViewSet,
    ChatSessionViewSet,
    ChatMessageViewSet,
    UsageLogViewSet,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="API para LLM",
      default_version='v1',
      description="Documentação da API para o projeto de LLM",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contato@dominio.com"),
      license=openapi.License(name="Licença MIT"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r'requests', LLMRequestViewSet, basename='llmrequest')
router.register(r'configs', LLMConfigViewSet, basename='llmconfig')
router.register(r'chatsessions', ChatSessionViewSet, basename='chatsession')
router.register(r'chatmessages', ChatMessageViewSet, basename='chatmessage')
router.register(r'usagelogs', UsageLogViewSet, basename='usagelog')

urlpatterns = [
    path('', include(router.urls)),  # Roteamento para os endpoints
]