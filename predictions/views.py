from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .services import predecir_rendimiento, reentrenar_modelo
from .serializers import PredictionInputSerializer


class PredictView(APIView):
    """
    Endpoint de predicción de rendimiento.
    El atleta manda sus parámetros del día y recibe
    una estimación de su tiempo en el WOD.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PredictionInputSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Añadimos los datos del perfil del usuario autenticado
        datos_entrada = serializer.validated_data
        datos_entrada["peso_kg"] = request.user.peso_kg or 75.0
        datos_entrada["altura_cm"] = request.user.altura_cm or 175.0

        try:
            prediccion = predecir_rendimiento(datos_entrada)
        except ValueError as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        return Response(
            {
                "tiempo_estimado_minutos": prediccion,
                "mensaje": f"Tu rendimiento estimado para hoy es de {prediccion} minutos.",
            },
            status=status.HTTP_200_OK,
        )


class RetrainView(APIView):
    """
    Endpoint interno de reentrenamiento autónomo.
    Solo accesible por administradores — recoge los datos reales
    de PostgreSQL y reentrena el modelo en caliente.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Solo los admins pueden reentrenar
        if not request.user.is_staff:
            return Response(
                {"error": "Solo los administradores pueden reentrenar el modelo."},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            r2 = reentrenar_modelo()
        except Exception as e:
            return Response(
                {"error": f"Error durante el reentrenamiento: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {
                "mensaje": "Modelo reentrenado correctamente.",
                "r2_score": r2,
            },
            status=status.HTTP_200_OK,
        )
