# WODAnalytics AI 🏋️‍♂️

API REST para la gestión de entrenamientos de CrossFit y entrenamiento híbrido, con integración de Machine Learning para predicción de rendimiento.

## 🛠️ Stack Tecnológico

- **Backend:** Python 3.13, Django, Django REST Framework
- **Base de datos:** PostgreSQL 15
- **Autenticación:** JWT (djangorestframework-simplejwt)
- **IA/ML:** Scikit-Learn, Pandas, NumPy, Joblib
- **DevOps:** Docker, Docker Compose
- **Testing:** Pytest, pytest-django

## 🚀 Instalación y Ejecución

### Requisitos previos
- Docker Desktop instalado y corriendo

### Pasos

1. Clona el repositorio:
```bash
git clone https://github.com/Alejandro-Iglesias/WODanalytics.git
cd WODanalytics
```

2. Crea el archivo `.env` en la raíz con estas variables:

SECRET_KEY=tu_secret_key
DEBUG=1
DB_NAME=wodanalytics
DB_USER=woduser
DB_PASSWORD=wodpass
DB_HOST=db
DB_PORT=5432

3. Levanta los contenedores:
```bash
docker-compose up --build
```

4. Aplica las migraciones:
```bash
docker-compose exec api python manage.py migrate
```

5. La API estará disponible en `http://localhost:8000`

## 📡 Endpoints Principales

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
| GET | `/api/v1/wods/` | Historial de WODs + racha + alerta de fatiga | Sí |
| POST | `/api/v1/wods/` | Registrar un nuevo WOD | Sí |
| GET | `/api/v1/wods/metricas/` | Métricas de recuperación | Sí |
| POST | `/api/v1/wods/metricas/` | Registrar métricas de recuperación | Sí |

### Predicciones (próximamente)
| Método | Endpoint | Descripción | Token |
|--------|----------|-------------|-------|
| POST | `/api/v1/predict/` | Predicción de rendimiento con ML | Sí |

## 🧠 Lógica de Negocio

- **Algoritmo de Rachas:** calcula días consecutivos de entrenamiento
- **Media Semanal:** promedio de entrenamientos en los últimos 7 días
- **Alerta de Fatiga:** detecta riesgo de sobreentrenamiento analizando volumen de las últimas 48h y métricas de recuperación

## 🔒 Seguridad

- Autenticación stateless con JWT
- Aislamiento de datos por usuario
- Validación de contraseñas con expresiones regulares
- Variables de entorno para datos sensibles

## 📁 Estructura del Proyecto


\```
wodanalytics/
├── config/          # Configuración Django
├── users/           # App de autenticación y usuarios
├── wods/            # App de entrenamientos y métricas
├── predictions/     # App de ML (en desarrollo)
├── docs/            # Documentación y colección Postman
├── ml_model/        # Modelos y scripts de ML
├── frontend/        # Dashboard HTML/Tailwind/JS
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
\```

## 📚 Documentación

- Colección Postman: `docs/WODAnalytics.postman_collection.json`
- Casos de prueba: `docs/testing.md`

## 👨‍💻 Autor

**Alejandro Iglesias Estévez** — Python Backend Developer
[LinkedIn](www.linkedin.com/in/alejandro-iglesias-estévez-a9a157239) · [GitHub](https://github.com/Alejandro-Iglesias)