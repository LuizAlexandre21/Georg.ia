from django.urls import path,include 
from rest_framework.routers import DefaultRouter
from .views import EmpresaView, UsuarioView
from rest_framework import permissions


urlpatterns = [
    # URL para a empresa
    path('empresas/', EmpresaView.as_view(), name='empresa-list'),
    path('empresas/<int:pk>/', EmpresaView.as_view(), name='empresa-detail'),
    
    # URL para os usuários (registro e operações)
    path('usuarios/', UsuarioView.as_view(), name='usuario-list'),  # Registro de usuário via POST
    path('usuarios/<int:pk>/', UsuarioView.as_view(), name='usuario-detail'),
]    
'''
    # URL para login
    path('login/', LoginViewSet.as_view(), name='login'),
    
    # URL para logout
    path('logout/', LogoutViewSet.as_view(), name='logout'),
]'
'''