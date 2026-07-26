from django.urls import path
from .views import MetricaRecuperacionListCreateView, WodListCreateView, WodDetailView

urlpatterns = [
    # --- Endpoints de entrenamientos ---
    path("", WodListCreateView.as_view(), name="wod-list-create"),
    # --- Endpoints de métricas de recuperación ---
    path("<int:pk>/", WodDetailView.as_view(), name="wod-detail"),
    path(
        "metricas/",
        MetricaRecuperacionListCreateView.as_view(),
        name="metrica-list-create",
    ),
]
