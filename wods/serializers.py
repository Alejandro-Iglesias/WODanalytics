from rest_framework import serializers
from .models import Wod, MetricaRecuperacion


class WodSerializer(serializers.ModelSerializer):
    """
    Serializer para el registro y consulta de entrenamientos.
    El usuario se asigna automáticamente desde la vista — no se expone en la API.
    """

    class Meta:
        model = Wod
        fields = [
            "id",
            "nombre_ejercicio",
            "tipo",
            "resultado_tiempo",
            "resultado_repeticiones",
            "peso",
            "notas",
            "fecha_entrenamiento",
            "fecha_creacion",
        ]
        read_only_fields = ["fecha_entrenamiento", "fecha_creacion"]

    def validate(self, data):
        """
        Validación cruzada entre campos — usamos validate() en vez de
        validate_campo() porque la lógica depende de varios campos a la vez.
        """
        tipo = data.get("tipo")
        resultado_tiempo = data.get("resultado_tiempo")
        resultado_repeticiones = data.get("resultado_repeticiones")

        if tipo == "for_time" and not resultado_tiempo:
            raise serializers.ValidationError(
                {
                    "resultado_tiempo": "Los WODs For Time requieren un resultado de tiempo."
                }
            )
        if tipo == "amrap" and not resultado_repeticiones:
            raise serializers.ValidationError(
                {
                    "resultado_repeticiones": "Los WODs AMRAP requieren un resultado de repeticiones."
                }
            )
        return data


class MetricaRecuperacionSerializer(serializers.ModelSerializer):
    """
    Serializer para el registro y consulta de métricas de recuperación diarias.
    """

    class Meta:
        model = MetricaRecuperacion
        fields = [
            "id",
            "fecha",
            "horas_sueno",
            "fatiga_muscular",
            "nivel_estres",
            "fecha_creacion",
        ]
        read_only_fields = ["fecha", "fecha_creacion"]

    def validate_fatiga_muscular(self, value):
        # Validamos que la fatiga esté en el rango permitido
        if not 1 <= value <= 10:
            raise serializers.ValidationError(
                "La fatiga muscular debe estar entre 1 y 10."
            )
        return value

    def validate_nivel_estres(self, value):
        # Validamos que el estrés esté en el rango permitido
        if not 1 <= value <= 10:
            raise serializers.ValidationError(
                "El nivel de estrés debe estar entre 1 y 10."
            )
        return value
