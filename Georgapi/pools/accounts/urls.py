from django.urls import path,include 
from rest_framework.routers import DefaultRouter
from .views import LoginView,LogoutView, RegisterUserView,UserViewSet,DeleteUserView
from rest_framework import permissions

router = DefaultRouter()
router.register(r'users', UserViewSet)  # Apenas o ViewSet aqui


urlpatterns = [
    path('', include(router.urls)),           # Rotas do UserViewSet
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('delete_user',DeleteUserView.as_view(),name = "delete")
]