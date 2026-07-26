import os
import sys
import django
import numpy as np
import pandas as pd

# --- Configuración de Django para poder usar los modelos fuera del servidor ---
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model
from wods.models import Wod, MetricaRecuperacion

User = get_user_model()

np.random.seed(42)
N = 500  # Número de registros a generar


def generar_dataset():
    """
    Genera un dataset sintético de entrenamientos de CrossFit.
    El target (resultado_tiempo) se calcula con una fórmula que simula
    la realidad: más fatiga + menos sueño + más estrés = peor resultado.
    """

    # --- Generación de variables independientes ---
    edad = np.random.randint(20, 45, N)
    peso_kg = np.random.uniform(55, 100, N).round(1)
    altura_cm = np.random.uniform(160, 195, N).round(1)
    horas_sueno = np.random.uniform(4, 9, N).round(1)
    fatiga_muscular = np.random.randint(1, 11, N)
    nivel_estres = np.random.randint(1, 11, N)
    dias_entrenando = np.random.randint(1, 31, N)

    TIPOS = ["for_time", "amrap", "emom", "tabata"]
    tipo_wod = np.random.choice(TIPOS, N)
    tipo_wod_num = np.where(
        tipo_wod == "for_time",
        0,
        np.where(tipo_wod == "amrap", 1, np.where(tipo_wod == "emom", 2, 3)),
    )

    # --- Cálculo del target con fórmula realista ---
    # Base: 10 minutos
    # Penalizaciones: fatiga, estrés, poco sueño
    # Bonificaciones: más días entrenando, mejor condición física
    resultado_tiempo = (
        10
        + fatiga_muscular * 0.8
        + nivel_estres * 0.5
        - horas_sueno * 0.6
        - dias_entrenando * 0.1
        + (edad - 30) * 0.05
        + np.random.normal(0, 1, N)  # ruido aleatorio realista
    ).round(2)

    # Garantizamos que no haya tiempos negativos
    resultado_tiempo = np.clip(resultado_tiempo, 1, 60)

    # --- Creación del DataFrame ---
    df = pd.DataFrame(
        {
            "edad": edad,
            "peso_kg": peso_kg,
            "altura_cm": altura_cm,
            "horas_sueno": horas_sueno,
            "fatiga_muscular": fatiga_muscular,
            "nivel_estres": nivel_estres,
            "dias_entrenando": dias_entrenando,
            "tipo_wod": tipo_wod,
            "tipo_wod_num": tipo_wod_num,
            "resultado_tiempo": resultado_tiempo,
        }
    )

    # --- Guardamos el CSV ---
    csv_path = os.path.join(os.path.dirname(__file__), "dataset.csv")
    df.to_csv(csv_path, index=False)
    print(f"Dataset guardado en {csv_path}")
    print(f"{N} registros generados")
    print(df.describe())

    # --- Volcado en PostgreSQL ---
    volcar_en_postgresql(df)

    return df


def volcar_en_postgresql(df):
    """
    Vuelca los datos simulados en PostgreSQL usando el modelo Wod y
    MetricaRecuperacion de Django. Crea un usuario de prueba si no existe.
    """
    print("\n Volcando datos en PostgreSQL...")

    # Creamos o recuperamos el usuario de prueba
    usuario, creado = User.objects.get_or_create(
        username="atleta_simulado",
        defaults={
            "email": "simulado@wodanalytics.com",
            "peso_kg": 75.0,
            "altura_cm": 180.0,
        },
    )
    if creado:
        usuario.set_password("Simulado1234!")
        usuario.save()
        print("Usuario de prueba creado: atleta_simulado")
    else:
        print("Usuario de prueba ya existe: atleta_simulado")

    # Volcamos los WODs
    wods_creados = 0
    metricas_creadas = 0

    for _, row in df.iterrows():
        Wod.objects.create(
            usuario=usuario,
            nombre_ejercicio=f"WOD Simulado {row['tipo_wod'].upper()}",
            tipo=row["tipo_wod"],
            resultado_tiempo=float(row["resultado_tiempo"]),
            notas=f"Dato simulado — fatiga: {row['fatiga_muscular']}/10",
        )
        wods_creados += 1

        MetricaRecuperacion.objects.create(
            usuario=usuario,
            horas_sueno=float(row["horas_sueno"]),
            fatiga_muscular=int(row["fatiga_muscular"]),
            nivel_estres=int(row["nivel_estres"]),
        )
        metricas_creadas += 1

    print(f"{wods_creados} WODs volcados en PostgreSQL")
    print(f"{metricas_creadas} métricas volcadas en PostgreSQL")


if __name__ == "__main__":
    generar_dataset()
