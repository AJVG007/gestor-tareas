from django.urls import path
from .views import *

urlpatterns = [
    path('register/', UsuarioRegisterView.as_view(), name='usuario-register'),
    path('login/', LoginView.as_view(), name='usuario-login'),
    path('details/', UserDetailsViews.as_view(), name='usuario-details')
]
