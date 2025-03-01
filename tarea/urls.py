from django.urls import path
from .views import (
    TareaListView,
    TareaCreateView,
    TareaDetailView,
    TareaUpdateView,
    TareaDeleteView,
    TareaFilterCompletedView
)

urlpatterns = [
    path('list', TareaListView.as_view(), name='tarea-list'),
    path('create', TareaCreateView.as_view(), name='tarea-create'),
    path('detail/<int:pk>', TareaDetailView.as_view(), name='tarea-detail'),
    path('update/<int:pk>', TareaUpdateView.as_view(), name='tarea-update'),
    path('delete/<int:pk>', TareaDeleteView.as_view(), name='tarea-delete'),
    path('filter/completed', TareaFilterCompletedView.as_view(), name='tarea-filter-completed'),
] 