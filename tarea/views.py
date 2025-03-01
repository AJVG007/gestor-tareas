from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Tarea
from .serializers import TareaSerializer

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user

class TareaListView(generics.ListAPIView):
    """
    List all tareas for the authenticated user.
    """
    serializer_class = TareaSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Tarea.objects.filter(owner=self.request.user)

class TareaCreateView(generics.CreateAPIView):
    """
    Create a new tarea for the authenticated user.
    """
    serializer_class = TareaSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TareaDetailView(generics.RetrieveAPIView):
    """
    Retrieve a tarea instance.
    """
    serializer_class = TareaSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    
    def get_queryset(self):
        return Tarea.objects.filter(owner=self.request.user)

class TareaUpdateView(generics.UpdateAPIView):
    """
    Update a tarea instance. Only title, description, and completed fields can be updated.
    """
    serializer_class = TareaSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    http_method_names = ['patch']
    
    def get_queryset(self):
        return Tarea.objects.filter(owner=self.request.user)
    
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        
        allowed_fields = ['title', 'description', 'completed']
        data = {}
        invalid_fields = []
        
        for field in request.data:
            if field in allowed_fields:
                data[field] = request.data[field]
            else:
                invalid_fields.append(field)
        
        if invalid_fields:
            return Response(
                {
                    "error": f"Invalid fields: {', '.join(invalid_fields)}. Only title, description, and completed can be updated."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not data:
            return Response(
                {"error": "No valid fields to update. Only title, description, and completed can be updated."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)

class TareaDeleteView(generics.DestroyAPIView):
    """
    Delete a tarea instance.
    """
    serializer_class = TareaSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    
    def get_queryset(self):
        return Tarea.objects.filter(owner=self.request.user)

class TareaFilterCompletedView(generics.ListAPIView):
    """
    List all completed tareas for the authenticated user.
    """
    serializer_class = TareaSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Tarea.objects.filter(owner=self.request.user, completed=True)
