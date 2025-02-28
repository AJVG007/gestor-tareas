from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed
import logging

logger = logging.getLogger(__name__) # Get a logger instance

class JWTAuthenticationFromCookie(JWTAuthentication):
    def get_jwt_value(self, request):
        auth_cookie = request.COOKIES.get('access_token_cookie')
        logger.debug(f"JWTAuthenticationFromCookie: Cookie 'access_token_cookie' value: {auth_cookie}") # Log cookie value

        if not auth_cookie:
            logger.debug("JWTAuthenticationFromCookie: Cookie 'access_token_cookie' not found in request") # Log if cookie is missing
            return None

        return auth_cookie

    def authenticate(self, request):
        validated_token = None
        try:
            validated_token = self.get_validated_token(self.get_jwt_value(request))
            logger.debug(f"JWTAuthenticationFromCookie: Token validation successful for token: {validated_token}") # Log successful validation
        except AuthenticationFailed as e:
            logger.debug(f"JWTAuthenticationFromCookie: Authentication failed: {e}") # Log authentication failure
            raise # Re-raise the exception so DRF handles the 403

        if not validated_token:
            logger.debug("JWTAuthenticationFromCookie: Validated token is None (authentication failed)")
            raise AuthenticationFailed('No valid token found in cookie')


        user, _ = self.authenticate_credentials(validated_token)
        logger.debug(f"JWTAuthenticationFromCookie: Authenticated user: {user}") # Log authenticated user
        return (user, validated_token)