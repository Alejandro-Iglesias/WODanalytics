# WODAnalytics AI

API REST para la gestión de entrenamientos de CrossFit y entrenamiento híbrido, con integración de Machine Learning para predicción de rendimiento.

## Stack Tecnológico

- **Backend:** Python 3.13, Django, Django REST Framework
- **Base de datos:** PostgreSQL 15
- **Autenticación:** JWT (djangorestframework-simplejwt)
- **IA/ML:** Scikit-Learn, Pandas, NumPy, Joblib
- **DevOps:** Docker, Docker Compose
- **Testing:** Pytest, pytest-django — 22 tests
- **Frontend:** React, Tailwind CSS
- **Documentación:** drf-spectacular (Swagger/OpenAPI)

## Instalación y Ejecución

### Requisitos previos
- Docker Desktop instalado y corriendo
- Node.js v18+ instalado

### Backend

1. Clona el repositorio:
```bash
git clone https://github.com/Alejandro-Iglesias/WODanalytics.git
cd WODanalytics
```

2. Crea el archivo `.env` en la raíz:
```
SECRET_KEY=tu_secret_key
DEBUG=1
DB_NAME=wodanalytics
DB_USER=woduser
DB_PASSWORD=wodpass
DB_HOST=db
DB_PORT=5432
```

3. Levanta los contenedores:
```bash
docker-compose up --build
```

4. Aplica las migraciones:
```bash
docker-compose exec api python manage.py migrate
```

5. Genera los datos de entrenamiento y entrena el modelo ML:
```bash
docker-compose exec api python ml_model/dataset_simulation.py
docker-compose exec api python ml_model/train.py
```

6. La API estará disponible en `http://localhost:8000`

### Frontend

**1. Entra en la carpeta del frontend:**
```bash
cd frontend
```
**2. Instala las dependencias:**
```bash
npm install
```
**3. Arranca el servidor de desarrollo:**
```bash
npm run dev
```
**4. El dashboard estará disponible en** `http://localhost:5173`

## Endpoints Principales

### Autenticación
| Método | Endpoint | Descripción | Token |
|--------|----------|-------------|-------|
| POST | `/api/v1/auth/register/` | Registro de nuevos atletas | No |
| POST | `/api/v1/auth/token/` | Login — devuelve Access y Refresh Token | No |
| POST | `/api/v1/auth/token/refresh/` | Refresca el Access Token | No |
| GET | `/api/v1/auth/profile/` | Perfil del atleta autenticado | Sí |

### Entrenamientos
| Método | Endpoint | Descripción | Token |
|--------|----------|-------------|-------|
| GET | `/api/v1/wods/` | Historial + racha + alerta de fatiga | Sí |
| POST | `/api/v1/wods/` | Registrar un nuevo WOD | Sí |
| GET | `/api/v1/wods/{id}/` | Detalle de un WOD | Sí |
| PUT | `/api/v1/wods/{id}/` | Editar un WOD | Sí |
| DELETE | `/api/v1/wods/{id}/` | Eliminar un WOD | Sí |
| GET | `/api/v1/wods/metricas/` | Métricas de recuperación | Sí |
| POST | `/api/v1/wods/metricas/` | Registrar métricas de recuperación | Sí |

### Predicciones
| Método | Endpoint | Descripción | Token |
|--------|----------|-------------|-------|
| POST | `/api/v1/predict/` | Predicción de rendimiento con ML | Sí |
| POST | `/api/v1/predict/retrain/` | Reentrenamiento del modelo (Admin) | Sí |

## Lógica de Negocio

- **Algoritmo de Rachas:** calcula días consecutivos de entrenamiento
- **Media Semanal:** promedio de entrenamientos en los últimos 7 días
- **Alerta de Fatiga:** detecta riesgo de sobreentrenamiento analizando volumen de las últimas 48h y métricas de recuperación
- **Predicción ML:** Random Forest Regressor con R²=0.7469

## Seguridad

- Autenticación stateless con JWT
- Aislamiento de datos por usuario
- Validación de contraseñas con expresiones regulares
- Variables de entorno para datos sensibles

## Testing

```bash
docker-compose exec api pytest tests/ -v
```

22 tests cubriendo users, wods y predictions.

## Estructura del Proyecto

```
wodanalytics/
├── config/          # Configuración Django
├── users/           # App de autenticación y usuarios
├── wods/            # App de entrenamientos y métricas
├── predictions/     # App de predicción ML
├── tests/           # Tests con Pytest
├── docs/            # Documentación
├── ml_model/        # Scripts y modelos de ML
├── frontend/        # Dashboard React + Tailwind CSS
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Documentación

- Swagger UI: `http://localhost:8000/api/docs/`
- Schema OpenAPI:`http://localhost:8000/api/schema/`
- Colección Postman: `docs/WODAnalytics.postman_collection.json`
- Casos de prueba: `docs/testing.md`
- Schema OpenAPI: `docs/WODAnalyticsAPI_openapi.yaml`

## Autor

**Alejandro Iglesias Estévez** — Python Backend Developer
[LinkedIn](https://www.linkedin.com/in/alejandroiglesias-estevez-a9a157239) · [GitHub](https://github.com/Alejandro-Iglesias)