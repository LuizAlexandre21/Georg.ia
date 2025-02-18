from django.urls import path,include 
from rest_framework.routers import DefaultRouter
from .views import LLMRequestViewSet,LLMConfigViewSet,LLMSessionViewSet,LLMLogViewSet,LLMUserinfo
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="Georg.ia -",
      default_version='v1',
      description="Documentação da API para o projeto de LLM Gestão Eficiente de Orçamentos e Recursos Governamentais com Inteligência Artificial",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="luizalexandre21@outlook.com"),
      license=openapi.License(name="Licença MIT"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r'requests', LLMRequestViewSet, basename='llmrequest')
router.register(r'configs', LLMConfigViewSet, basename='llmconfig')
router.register(r'chatsessions', LLMSessionViewSet, basename='chatsession')
router.register(r'usagelogs', LLMLogViewSet, basename='usagelog')
router.register(r'user_info',LLMUserinfo,basename='user_info'),

urlpatterns = [
    path('', include(router.urls)),  # Roteamento para os endpoints
]