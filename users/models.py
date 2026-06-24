from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Modelo de usuario personalizado que extiende AbstractUser.
    Usa email como campo de autenticación principal en vez de username.
    """

    # --- Campos personalizados del atleta ---

    email = models.EmailField(unique=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    peso_kg = models.FloatField(null=True, blank=True)
    altura_cm = models.FloatField(null=True, blank=True)
    # --- Metadatos ---
    fecha_registro = models.DateTimeField(auto_now_add=True)

    # --- Configuración de autenticación ---

    USERNAME_FIELD = "email"  # Login con email en vez de username
    REQUIRED_FIELDS = ["username"]

    class Meta:
        db_table = "users"

    def __str__(self) -> str:
        return f"{self.username} - {self.email}"
