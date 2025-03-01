from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken

class JWTAuthenticationFromCookie(JWTAuthentication):
    def get_jwt_value(self, request):
        auth_cookie = request.COOKIES.get('access_token_cookie')
        if not auth_cookie:
            return None
        return auth_cookie

    def authenticate(self, request):
        raw_token = self.get_jwt_value(request)
        if raw_token is None:
            return None
        
        validated_token = None
        try:
            validated_token = self.get_validated_token(raw_token)
        except InvalidToken:
            raise

        if not validated_token:
            raise AuthenticationFailed('No valid token found in cookie')

        user = self.get_user(validated_token)
        return (user, validated_token)