from rest_framework import serializers


class PredictionInputSerializer(serializers.Serializer):
    """
    Valida los datos de entrada para el endpoint de predicción.
    El atleta manda sus parámetros del día y el modelo estima su rendimiento.
    """

    # --- Parámetros del día ---
    fatiga_muscular = serializers.IntegerField(
        min_value=1, max_value=10, help_text="Nivel de fatiga muscular del 1 al 10"
    )
    nivel_estres = serializers.IntegerField(
        min_value=1, max_value=10, help_text="Nivel de estrés del 1 al 10"
    )
    horas_sueno = serializers.FloatField(
        min_value=0, max_value=24, help_text="Horas de sueño de la noche anterior"
    )
    tipo_wod = serializers.ChoiceField(
        choices=["for_time", "amrap", "emom", "tabata"],
        help_text="Tipo de WOD que va a realizar",
    )
