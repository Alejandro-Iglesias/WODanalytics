from django.contrib import admin
from .models import Wod, MetricaRecuperacion


@admin.register(Wod)
class WodAdmin(admin.ModelAdmin):
    """
    Panel de administración para el modelo Wod.
    """

    list_display = ["usuario", "nombre_ejercicio", "tipo", "fecha_entrenamiento"]
    list_filter = ["tipo", "fecha_entrenamiento"]
    search_fields = ["usuario__username", "nombre_ejercicio"]


@admin.register(MetricaRecuperacion)
class MetricaRecuperacionAdmin(admin.ModelAdmin):
    """
    Panel de administración para el modelo MetricaRecuperacion.
    """

    list_display = [
        "usuario",
        "fecha",
        "horas_sueno",
        "fatiga_muscular",
        "nivel_estres",
    ]
    list_filter = ["fecha"]
    search_fields = ["usuario__username"]
