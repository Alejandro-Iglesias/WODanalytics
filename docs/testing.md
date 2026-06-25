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