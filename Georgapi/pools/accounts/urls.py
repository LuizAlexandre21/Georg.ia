from django.urls import path
from .views import EmpresaView, UsuarioView
from .admin import RegisterView, LoginView, LogoutView

urlpatterns = [
    # URL para Empresas
    path('empresas/', EmpresaView.as_view(), name='empresa-list'),
    path('empresas/<int:pk>/', EmpresaView.as_view(), name='empresa-detail'),

    # URL para Usuários
    path('usuarios/', UsuarioView.as_view(), name='usuario-list'),
    path('usuarios/<int:pk>/', UsuarioView.as_view(), name='usuario-detail'),

    path('register/', RegisterView.as_view(), name='register'),  # URL para o registro do usuário
    path('login/', LoginView.as_view(), name='login'),  # URL para o login
    path('logout/', LogoutView.as_view(), name='logout'),  # URL para o logout
]