from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Wod, MetricaRecuperacion
from .serializers import WodSerializer, MetricaRecuperacionSerializer


class WodListCreateView(generics.ListCreateAPIView):
    """
    GET  → devuelve el historial de WODs del atleta autenticado.
    POST → registra un nuevo WOD para el atleta autenticado.
    """

    serializer_class = WodSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filtramos por el usuario autenticado — aislamiento de datos
        return Wod.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        # Asignamos el usuario autenticado automáticamente al crear un WOD
        serializer.save(usuario=self.request.user)


class MetricaRecuperacionListCreateView(generics.ListCreateAPIView):
    """
    GET  → devuelve las métricas de recuperación del atleta autenticado.
    POST → registra una nueva métrica de recuperación.
    """

    serializer_class = MetricaRecuperacionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filtramos por el usuario autenticado — aislamiento de datos
        return MetricaRecuperacion.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        # Asignamos el usuario autenticado automáticamente
        serializer.save(usuario=self.request.user)
