import os
import joblib
from django.apps import AppConfig


class PredictionsConfig(AppConfig):
    """
    Configuración de la app predictions.
    Carga el modelo de ML en memoria RAM al arrancar el servidor
    para garantizar respuestas instantáneas en el endpoint de predicción.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "predictions"

    # Variable de clase donde almacenamos el modelo en memoria
    modelo = None

    def ready(self):
        """
        Se ejecuta una sola vez cuando Django arranca.
        Carga el modelo .joblib en memoria RAM.
        """
        model_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "ml_model",
            "modelo_rendimiento.joblib",
        )

        if os.path.exists(model_path):
            PredictionsConfig.modelo = joblib.load(model_path)
            print("Modelo de ML cargado en memoria RAM correctamente")
        else:
            print("Modelo de ML no encontrado — ejecuta ml_model/train.py primero")
