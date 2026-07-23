import os
import joblib
import pandas as pd
from predictions.apps import PredictionsConfig

# Mapa de encoding del tipo de WOD — debe coincidir con el usado en train.py
TIPO_WOD_MAP = {"for_time": 0, "amrap": 1, "emom": 2, "tabata": 3}


def predecir_rendimiento(datos_entrada: dict) -> float:
    """
    Realiza una predicción de rendimiento usando el modelo Random Forest
    cargado en memoria RAM.

    Args:
        datos_entrada: diccionario con los campos del atleta para la predicción

    Returns:
        float: tiempo estimado en minutos
    """
    modelo = PredictionsConfig.modelo

    if modelo is None:
        raise ValueError(
            "El modelo no está cargado. Ejecuta ml_model/train.py primero."
        )

    # --- Encoding del tipo de WOD ---
    tipo_wod = datos_entrada.get("tipo_wod", "for_time")
    tipo_wod_num = TIPO_WOD_MAP.get(tipo_wod, 0)

    # --- Construcción del DataFrame con el mismo orden de features del entrenamiento ---
    df_entrada = pd.DataFrame(
        [
            {
                "fatiga_muscular": datos_entrada["fatiga_muscular"],
                "nivel_estres": datos_entrada["nivel_estres"],
                "horas_sueno": datos_entrada["horas_sueno"],
                "tipo_num": tipo_wod_num,
                "usuario__peso_kg": datos_entrada.get("peso_kg", 75.0),
                "usuario__altura_cm": datos_entrada.get("altura_cm", 175.0),
            }
        ]
    )

    # --- Predicción ---
    prediccion = modelo.predict(df_entrada)[0]

    return round(float(prediccion), 2)


def reentrenar_modelo() -> float:
    """
    Reentrena el modelo Random Forest con los datos reales acumulados
    en PostgreSQL y recarga el modelo en memoria sin reiniciar el servidor.

    Returns:
        float: R² del modelo reentrenado
    """
    import sys

    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    from ml_model.train import cargar_datos, preparar_features, entrenar_modelo

    # --- Reentrenamiento ---
    df_wods, df_metricas = cargar_datos()
    X, y = preparar_features(df_wods, df_metricas)
    _, r2 = entrenar_modelo(X, y)

    # --- Recarga del modelo en memoria sin reiniciar ---
    model_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "ml_model",
        "modelo_rendimiento.joblib",
    )
    PredictionsConfig.modelo = joblib.load(model_path)
    print("Modelo recargado en memoria RAM tras reentrenamiento")

    return r2
