from django.db import models

    
class Tarea(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    #owner = models.ForeignKey(Usuario, on_delete=models.CASCADE)
