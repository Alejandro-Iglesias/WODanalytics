from django.urls import path
from .views import MetricaRecuperacionListCreateView, WodListCreateView

urlpatterns = [
    # --- Endpoints de entrenamientos ---
    path("", WodListCreateView.as_view(), name="wod-list-create"),
    # --- Endpoints de métricas de recuperación ---
    path(
        "metricas/",
        MetricaRecuperacionListCreateView.as_view(),
        name="metrica-list-create",
    ),
]
