from django.urls import path
from .views import PredictView, RetrainView

urlpatterns = [
    # --- Endpoint de predicción de rendimiento ---
    path("", PredictView.as_view(), name="predict"),
    # --- Endpoint interno de reentrenamiento autónomo ---
    path("retrain/", RetrainView.as_view(), name="retrain"),
]
