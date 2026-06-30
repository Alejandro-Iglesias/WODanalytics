## Pruebas de la API

### POST /api/v1/auth/register/

| Caso | Descripción | Body | Resultado esperado |
|------|-------------|------|--------------------|

| 1 | Contraseña sin mayúscula | `{"password": "test1234!"}` | 400 - "Debe contener mayúscula" |
| 2 | Contraseña sin especial | `{"password": "Test1234"}` | 400 - "Debe contener al menos un carácter especial" |
| 3 | Email con mayúsculas | `{"email": "TEST@GMAIL.COM"}` | 201 - email en minúsculas |
| 4 | Email duplicado | email ya existente | 400 - email ya existe |
| 5 | Registro completo | todos los campos | 201 - usuario creado |

### POST /api/v1/auth/token/

| Caso | Descripción | Body | Resultado esperado |
|------|-------------|------|--------------------|

| 1 | Login correcto | `{"email": "carmen@gmail.com", "password": "Test1234!"}` | 200 - access + refresh token |
| 2 | Password incorrecta | `{"email": "alejandro-iglesias@gmail.com", "password": "wrongpass"}` | 401 - credenciales no válidas |

### GET /api/v1/auth/profile/

| Caso | Descripción | Header | Resultado esperado |
|------|-------------|--------|--------------------|

| 1 | Con token válido | `Authorization: Bearer <token>` | 200 - datos del perfil |
| 2 | Sin token | Sin header | 401 - no autenticado |


### POST /api/v1/wods/

| Caso | Descripción | Body | Resultado esperado |
|------|-------------|------|--------------------|
| 1 | Registrar WOD for_time | `{"nombre_ejercicio": "Murphy", "tipo": "for_time", "resultado_tiempo": 12.5}` | 201 - WOD creado |
| 2 | WOD for_time sin tiempo | `{"nombre_ejercicio": "Gimnasticos", "tipo": "for_time"}` | 400 - resultado_tiempo requerido |
| 3 | WOD AMRAP sin repeticiones | `{"nombre_ejercicio": "Sincros", "tipo": "amrap"}` | 400 - resultado_repeticiones requerido |

### GET /api/v1/wods/

| Caso | Descripción | Header | Resultado esperado |
|------|-------------|--------|--------------------|
| 1 | Listar WODs con token | Bearer Token válido | 200 - lista de WODs del atleta |
| 2 | Sin token | Sin header | 401 - no autenticado |

### POST /api/v1/wods/metricas/

| Caso | Descripción | Body | Resultado esperado |
|------|-------------|------|--------------------|
| 1 | Registrar métrica válida | `{"horas_sueno": 7.5, "fatiga_muscular": 6, "nivel_estres": 4}` | 201 - métrica creada |
| 2 | Fatiga fuera de rango | `{"fatiga_muscular": 11}` | 400 - debe estar entre 1 y 10 |

### GET /api/v1/wods/metricas/

| Caso | Descripción | Header | Resultado esperado |
|------|-------------|--------|--------------------|
| 1 | Listar métricas con token | Bearer Token válido | 200 - lista de métricas del atleta |