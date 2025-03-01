from rest_framework import views, permissions, generics, response, status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UsuarioSerializers
from users.models import Usuario

class UsuarioRegisterView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializers
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return response.Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        
        if not username or not password:
            return response.Response(
                {"error": "Username and password are required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            resp = response.Response(
                {"message": "Login successful"}, 
                status=status.HTTP_200_OK
            )
            
            resp.set_cookie(
                "access_token_cookie",
                value=access_token,
                httponly=True,
                samesite='Lax',
                max_age=300
            )
            
            resp.set_cookie(
                "refresh_token",
                value=refresh_token,
                httponly=True,
                samesite='Lax',
                max_age=86400
            )
            
            return resp
        else:
            return response.Response(
                {"error": "Invalid credentials"}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

class UserDetailsViews(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UsuarioSerializers(request.user)
        return response.Response(serializer.data)