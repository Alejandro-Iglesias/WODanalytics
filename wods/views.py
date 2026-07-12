from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Wod, MetricaRecuperacion
from .serializers import WodSerializer, MetricaRecuperacionSerializer
from .services import calcular_media_semanal, calcular_racha, evaluar_alerta_fatiga


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

    def list(self, request):
        racha = calcular_racha(request.user)
        media = calcular_media_semanal(request.user)
        fatiga = evaluar_alerta_fatiga(request.user)

        queryset = self.get_queryset()
        serializer = WodSerializer(queryset, many=True)

        return Response(
            {
                "racha_dias": racha,
                "media_semanal": media,
                "alerta_fatiga": fatiga,
                "wods": serializer.data,
            }
        )


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
