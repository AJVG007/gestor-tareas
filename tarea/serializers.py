from rest_framework import serializers
from .models import Tarea

class TareaSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    
    class Meta:
        model = Tarea
        fields = ['id', 'title', 'description', 'completed', 'created_at', 'owner']
        read_only_fields = ['id', 'created_at', 'owner']
        
    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters long.")
        return value 