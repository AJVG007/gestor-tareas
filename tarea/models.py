from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    is_active = models.BooleanField(default=True)
    groups = models.ManyToManyField(
        'auth.Group', 
        related_name='usuarios_tareas',
        blank=True, 
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', 
        verbose_name='groups',
        ) 
    user_permissions = models.ManyToManyField(
        'auth.Permission', 
        related_name='usuarios_tareas',
        blank=True, 
        help_text='Specific permissions for this user.', 
        verbose_name='user permissions', 
        )
    
    def __str__(self):
        return self.username
    
class Tarea(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(Usuario, on_delete=models.CASCADE)
