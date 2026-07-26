import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def usuario(db):
    return User.objects.create_user(
        username="testuser",
        email="test@gmail.com",
        password="Test1234!",
    )


@pytest.fixture
def admin(db):
    return User.objects.create_superuser(
        username="admin",
        email="admin@wodanalytics.com",
        password="Admin1234!",
    )


@pytest.fixture
def client_autenticado(client, usuario):
    url = reverse("token_obtain_pair")
    res = client.post(
        url,
        {
            "email": "test@gmail.com",
            "password": "Test1234!",
        },
        format="json",
    )
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {res.data['access']}")
    return client


@pytest.fixture
def client_admin(client, db):
    from wods.models import Wod, MetricaRecuperacion
    import random

    # Creamos el usuario atleta_simulado que usa train.py
    atleta = User.objects.create_user(
        username="atleta_simulado",
        email="simulado@wodanalytics.com",
        password="Simulado1234!",
    )

    # Creamos datos de prueba
    for i in range(10):
        Wod.objects.create(
            usuario=atleta,
            nombre_ejercicio=f"WOD {i}",
            tipo=random.choice(["for_time", "amrap", "emom", "tabata"]),
            resultado_tiempo=round(random.uniform(5, 30), 1),
        )
        MetricaRecuperacion.objects.create(
            usuario=atleta,
            horas_sueno=round(random.uniform(5, 9), 1),
            fatiga_muscular=random.randint(1, 10),
            nivel_estres=random.randint(1, 10),
        )

    # Creamos el admin
    admin = User.objects.create_superuser(
        username="admin",
        email="admin@wodanalytics.com",
        password="Admin1234!",
    )

    url = reverse("token_obtain_pair")
    res = client.post(
        url,
        {
            "email": "admin@wodanalytics.com",
            "password": "Admin1234!",
        },
        format="json",
    )
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {res.data['access']}")
    return client


@pytest.mark.django_db
class TestPredict:
    """Tests del endpoint de predicción de rendimiento."""

    def test_prediccion_valida(self, client_autenticado):
        """El modelo devuelve una predicción con datos válidos."""
        url = reverse("predict")
        res = client_autenticado.post(
            url,
            {
                "fatiga_muscular": 5,
                "nivel_estres": 4,
                "horas_sueno": 7.5,
                "tipo_wod": "for_time",
            },
            format="json",
        )
        assert res.status_code == 200
        assert "tiempo_estimado_minutos" in res.data
        assert "mensaje" in res.data
        assert isinstance(res.data["tiempo_estimado_minutos"], float)

    def test_prediccion_fatiga_fuera_rango(self, client_autenticado):
        """La predicción falla si la fatiga está fuera del rango 1-10."""
        url = reverse("predict")
        res = client_autenticado.post(
            url,
            {
                "fatiga_muscular": 11,
                "nivel_estres": 4,
                "horas_sueno": 7.5,
                "tipo_wod": "for_time",
            },
            format="json",
        )
        assert res.status_code == 400

    def test_prediccion_sin_token(self, client):
        """Sin token devuelve 401."""
        url = reverse("predict")
        res = client.post(
            url,
            {
                "fatiga_muscular": 5,
                "nivel_estres": 4,
                "horas_sueno": 7.5,
                "tipo_wod": "for_time",
            },
            format="json",
        )
        assert res.status_code == 401


@pytest.mark.django_db
class TestRetrain:
    """Tests del endpoint de reentrenamiento del modelo."""

    def test_retrain_como_admin(self, client_admin):
        """Un admin puede llamar al endpoint de reentrenamiento."""
        from unittest.mock import patch

        url = reverse("retrain")
        # Mockeamos la función de reentrenamiento para no depender de datos reales
        with patch("predictions.views.reentrenar_modelo", return_value=0.75):
            res = client_admin.post(url)
        assert res.status_code == 200
        assert "r2_score" in res.data

    def test_retrain_como_usuario_normal(self, client_autenticado):
        """Un usuario normal no puede reentrenar el modelo."""
        url = reverse("retrain")
        res = client_autenticado.post(url)
        assert res.status_code == 403
