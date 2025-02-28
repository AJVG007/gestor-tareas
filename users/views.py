from rest_framework import views, permissions, generics, response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UsuarioSerializers
from users.models import Usuario

class UsuarioRegisterView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializers
    permission_classes = [permissions.AllowAny]

class LoginView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            resp = response.Response(status=200)
            resp.set_cookie("access_token",value=access_token,httponly=True)
            resp.set_cookie("refresh_token",value=refresh_token,httponly=True)
            return resp
        else:
            return response.Response({"error": "invalid credencials"},status=401)

class UserDetailsViews(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        #print(request.user)
        serializer = UsuarioSerializers(request.user)
        return response.Response(serializer.data)