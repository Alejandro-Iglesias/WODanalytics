# Arquitectura de la App Predictions

## Flujo completo

### 1. Script de datos simulados
- Genera un dataset sintético de entrenamientos con Pandas y NumPy
- Lo vuelca directamente en PostgreSQL via Django ORM

### 2. Script de entrenamiento
- Lee los datos de PostgreSQL transformándolos en DataFrame de Pandas
- Entrena un modelo Random Forest con Scikit-Learn
- Serializa y guarda el modelo como archivo `.joblib`

### 3. Carga en memoria (apps.py)
- Al arrancar Django, `apps.py` carga el modelo `.joblib` en RAM
- Garantiza respuestas instantáneas sin leer disco en cada petición

### 4. Endpoint de predicción
- `POST /api/v1/predict/` recibe los parámetros del día del atleta
- El servicio preprocesa los datos con NumPy/Pandas
- El modelo predice el rendimiento esperado
- Devuelve la predicción en la respuesta JSON

### 5. Pipeline de reentrenamiento autónomo
- Endpoint interno protegido recoge datos reales de PostgreSQL
- Reentrena el modelo ejecutando `.fit()` con los nuevos datos
- Sobrescribe el archivo `.joblib` en caliente sin reiniciar el servidor