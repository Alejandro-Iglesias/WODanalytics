from datetime import date, timedelta  # represenacion de los dias (timedelta)
from .models import Wod, MetricaRecuperacion


def calcular_racha(usuario) -> int:
    """
    Calcula los días consecutivos de entrenamiento del atleta.
    Recorre las fechas de WODs desde hoy hacia atrás y cuenta
    cuántos días seguidos hay sin interrupciones.
    """

    # Obtenemos las fechas únicas de entrenamiento ordenadas descendentemente
    fechas = (
        Wod.objects.filter(usuario=usuario)
        .values_list("fecha_entrenamiento", flat=True)  # devuelve una lista plana
        .distinct()  # solo una unica fecha por dia
        .order_by("-fecha_entrenamiento")
    )
    if not fechas:
        return 0

    racha = 0

    hoy = date.today()  # Guardamos la fecha actual

    for fecha in fechas:
        if fecha == hoy or fecha == hoy - timedelta(days=1):
            racha += 1
            hoy = fecha - timedelta(days=1)
        else:
            # hay un hueco por lo tanto la racha se rompe
            break

    return racha


def calcular_media_semanal(usuario) -> float:
    """
    Calcular el promedio de entrenamientos en los últimos 7 días
    """

    hace_7_dias = date.today() - timedelta(days=7)

    total_wods = Wod.objects.filter(
        usuario=usuario, fecha_entrenamiento__gte=hace_7_dias
    ).count()

    return round(total_wods / 7, 2)


def evaluar_alerta_fatiga(usuario) -> str | None:
    """
    Evalua si el atleta esta en riesgo de sobreentrenamiento.
    Comprueba el volumen de las últimas 48h y las métricas de recuperacion.
    Devuelve un mensaje de warning si hay riesgo, o None si todo esta bien
    """

    hace_48h = date.today() - timedelta(days=2)

    # Contamos entrenamientos en las ultimas 48 horas
    wods_recientes = Wod.objects.filter(
        usuario=usuario, fecha_entrenamiento__gte=hace_48h
    ).count()

    # Obtenemos la última metrica de recuperación
    ultima_metrica = (
        MetricaRecuperacion.objects.filter(usuario=usuario).order_by("-fecha").first()
    )

    if not ultima_metrica:
        return None

    # Evaluamos el riesgo
    volumen_alto = wods_recientes >= 2
    fatiga_alta = ultima_metrica.fatiga_muscular > 7
    poco_sueno = ultima_metrica.horas_sueno < 6

    if volumen_alto and (fatiga_alta or poco_sueno):
        return (
            "Alerta de sobreentrenamiento: "
            f"Has entrenado {wods_recientes} veces en las últimas 48h con fatiga alta "
            f"({ultima_metrica.fatiga_muscular}/10) de fatiga muscular"
            f"({ultima_metrica.horas_sueno}h) de sueño, considera descansar."
        )

    return None
