from django.db import models
from django.core.exceptions import ValidationError
from users.models import Usuario

def validate_title_length(value):
    if len(value) < 3:
        raise ValidationError('Title must be at least 3 characters long.')
    
class Tarea(models.Model):
    title = models.CharField(max_length=255, validators=[validate_title_length])
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='tareas', null=True, blank=True)

    def __str__(self):
        return self.title
