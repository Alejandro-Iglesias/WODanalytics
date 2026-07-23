# ML Model — WODAnalytics AI

Documentación técnica del módulo de Machine Learning.

## 📁 Estructura

```
ml_model/
├── dataset_simulation.py  # Genera datos sintéticos y los vuelca en PostgreSQL
├── train.py               # Entrena el modelo Random Forest y guarda el .joblib
├── dataset.csv            # Dataset generado (no se sube a GitHub)
└── modelo_rendimiento.joblib  # Modelo entrenado (no se sube a GitHub)
```

## 📊 Dataset

El dataset se genera con `dataset_simulation.py` usando NumPy y Pandas.
Contiene 500 registros sintéticos de entrenamientos de CrossFit.

### Variables de entrada (features)

| Variable | Tipo | Rango | Descripción |
|----------|------|-------|-------------|
| `edad` | int | 20-45 | Edad del atleta |
| `peso_kg` | float | 55-100 | Peso en kg |
| `altura_cm` | float | 160-195 | Altura en cm |
| `horas_sueno` | float | 4-9 | Horas de sueño |
| `fatiga_muscular` | int | 1-10 | Nivel de fatiga |
| `nivel_estres` | int | 1-10 | Nivel de estrés |
| `dias_entrenando` | int | 1-30 | Días consecutivos entrenando |
| `tipo_wod_num` | int | 0-3 | Tipo de WOD codificado |

### Variable objetivo (target)

| Variable | Tipo | Descripción |
|----------|------|-------------|
| `resultado_tiempo` | float | Tiempo estimado en minutos |

### Fórmula del target

```
resultado_tiempo = 10
    + fatiga_muscular × 0.8
    + nivel_estres × 0.5
    - horas_sueno × 0.6
    - dias_entrenando × 0.1
    + (edad - 30) × 0.05
    + ruido_aleatorio
```

La fórmula simula la realidad — más fatiga, más estrés y menos sueño producen peor rendimiento (más tiempo).

## 🤖 Modelo

- **Algoritmo:** Random Forest Regressor (Scikit-Learn)
- **Métrica:** R² (coeficiente de determinación)
- **Serialización:** Joblib

## 🔄 Pipeline de Reentrenamiento

El modelo se puede reentrenar en caliente desde el endpoint interno:

```
POST /api/v1/predict/retrain/
```

Lee los datos reales de PostgreSQL, ejecuta `.fit()` y sobrescribe el `.joblib` sin reiniciar el servidor.

## ⚠️ Archivos ignorados por Git

`dataset.csv` y `modelo_rendimiento.joblib` no se suben a GitHub porque son archivos generados. Están listados en `.gitignore`.