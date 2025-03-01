from rest_framework import serializers
from .models import Usuario

class UsuarioSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'is_active']
        read_only_fields = ['id', 'is_active']
        extra_kwargs = {
            'email': {'required': True}
        }
    
    def validate_email(self, value):
        """
        Check that the email is unique.
        """
        user = self.context['request'].user if 'request' in self.context else None
        
        if self.instance and self.instance.email == value:
            return value
            
        if Usuario.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return value
    
    def create(self, validated_data):
        password = validated_data.pop("password")
        user = Usuario(**validated_data)
        user.set_password(password)
        user.save()
        return user