from django.db import models
from django.conf import settings


class Wod(models.Model):
    """
    Registra cada sesión de entrenamiento completada por el atleta.
    Es la fuente principal de datos para el modelo de ML.
    """

    TIPO_CHOICES = [
        ("for_time", "For Time (Por Tiempo)"),
        ("amrap", "AMRAP (As Many Rounds As Possible)"),
        ("emom", "EMOM (Every Minute On the Minute)"),
        ("tabata", "Tabata / Intervalos"),
    ]
    # --- Relación con el atleta ---
    usuario = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wods",
    )
    # --- Datos del entrenamiento ---
    fecha_entrenamiento = models.DateField(auto_now_add=True)
    nombre_ejercicio = models.CharField(max_length=50)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    # --- Resultados (opcionales según el tipo de WOD) ---
    resultado_repeticiones = models.IntegerField(null=True, blank=True)
    resultado_tiempo = models.FloatField(null=True, blank=True)
    peso = models.FloatField(null=True, blank=True)
    notas = models.TextField(null=True, blank=True)
    # --- Metadatos ---
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "WODs"
        ordering = ["-fecha_entrenamiento"]

    def __str__(self) -> str:
        return f"{self.usuario} - {self.nombre_ejercicio} ({self.fecha_entrenamiento})"


class MetricaRecuperacion(models.Model):
    """
    Registra el estado físico diario del atleta.
    Sus datos se combinan con los WODs
    """

    # --- Relación con el atleta ---
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="metricas_recuperacion",
    )
    # --- Métricas diarias ---
    fecha = models.DateField(auto_now_add=True)
    horas_sueno = models.FloatField(help_text="Horas de sueño de la noche anterior")
    fatiga_muscular = models.IntegerField(
        help_text="Nivel de fatiga muscular del 1 al 10"
    )
    nivel_estres = models.IntegerField(help_text="Nivel de estrés del 1 al 10")
    # --- Metadatos ---
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "metricas_recuperacion"
        ordering = ["-fecha"]

    def __str__(self) -> str:
        return f"{self.usuario} - {self.fecha} - Fatiga: {self.fatiga_muscular}/10"
