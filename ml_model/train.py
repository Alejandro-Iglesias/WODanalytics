import os
import sys
import django
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

# --- Configuración de Django ---
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from wods.models import Wod, MetricaRecuperacion
from django.contrib.auth import get_user_model

User = get_user_model()


def cargar_datos():
    """
    Lee los datos de entrenamiento directamente desde PostgreSQL
    usando el ORM de Django y los transforma en DataFrames de Pandas.
    """
    print("Cargando datos desde PostgreSQL...")

    # Leemos los WODs del usuario simulado
    wods_qs = Wod.objects.filter(usuario__username="atleta_simulado").values(
        "resultado_tiempo",
        "tipo",
        "usuario__peso_kg",
        "usuario__altura_cm",
    )

    # Leemos las métricas de recuperación
    metricas_qs = MetricaRecuperacion.objects.filter(
        usuario__username="atleta_simulado"
    ).values(
        "horas_sueno",
        "fatiga_muscular",
        "nivel_estres",
    )

    df_wods = pd.DataFrame(list(wods_qs))
    df_metricas = pd.DataFrame(list(metricas_qs))

    print(f"{len(df_wods)} WODs cargados")
    print(f"{len(df_metricas)} métricas cargadas")

    return df_wods, df_metricas


def preparar_features(df_wods, df_metricas):
    """
    Combina los DataFrames y prepara las features para el modelo.
    Convierte el tipo de WOD a número mediante encoding.
    """
    # Combinamos los dos DataFrames por índice
    df = pd.concat(
        [df_wods.reset_index(drop=True), df_metricas.reset_index(drop=True)], axis=1
    )

    # Encoding del tipo de WOD — convertimos texto a número
    tipo_map = {"for_time": 0, "amrap": 1, "emom": 2, "tabata": 3}
    df["tipo_num"] = df["tipo"].map(tipo_map)

    # Eliminamos filas con valores nulos
    df = df.dropna()

    # Features que usará el modelo
    features = [
        "fatiga_muscular",
        "nivel_estres",
        "horas_sueno",
        "tipo_num",
        "usuario__peso_kg",
        "usuario__altura_cm",
    ]

    X = df[features]
    y = df["resultado_tiempo"]

    print(f"Features: {features}")
    print(f"Shape del dataset: {X.shape}")

    return X, y


def entrenar_modelo(X, y):
    """
    Entrena un RandomForestRegressor con los datos preparados.
    Evalúa el rendimiento con R² y guarda el modelo en disco.
    """
    # Dividimos en train (80%) y test (20%)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print(f"\nEntrenando con {len(X_train)} muestras...")

    # Entrenamos el modelo
    modelo = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        n_jobs=-1,  # usa todos los núcleos del procesador
    )
    modelo.fit(X_train, y_train)

    # Evaluamos el modelo
    y_pred = modelo.predict(X_test)
    r2 = r2_score(y_test, y_pred)

    print(f"R² en test: {r2:.4f} ({r2*100:.1f}% de varianza explicada)")

    # Guardamos el modelo
    model_path = os.path.join(os.path.dirname(__file__), "modelo_rendimiento.joblib")
    joblib.dump(modelo, model_path)
    print(f"Modelo guardado en {model_path}")

    return modelo, r2


if __name__ == "__main__":
    df_wods, df_metricas = cargar_datos()
    X, y = preparar_features(df_wods, df_metricas)
    modelo, r2 = entrenar_modelo(X, y)
    print(f"\nEntrenamiento completado — R²: {r2:.4f}")
