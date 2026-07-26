import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from wods.models import Wod, MetricaRecuperacion

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
def client_autenticado(client, usuario):
    """Cliente con token JWT del usuario de prueba."""
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
def wod_creado(usuario):
    """Crea un WOD de prueba en la base de datos."""
    return Wod.objects.create(
        usuario=usuario,
        nombre_ejercicio="Fran",
        tipo="for_time",
        resultado_tiempo=12.5,
        notas="Test WOD",
    )


@pytest.mark.django_db
class TestWodListCreate:
    """Tests del endpoint de listado y creación de WODs."""

    def test_listar_wods_autenticado(self, client_autenticado, wod_creado):
        """El atleta autenticado puede ver su historial de WODs."""
        url = reverse("wod-list-create")
        res = client_autenticado.get(url)
        assert res.status_code == 200
        assert "wods" in res.data
        assert "racha_dias" in res.data
        assert "media_semanal" in res.data
        assert "alerta_fatiga" in res.data
        assert len(res.data["wods"]) == 1

    def test_listar_wods_sin_token(self, client):
        """Sin token devuelve 401."""
        url = reverse("wod-list-create")
        res = client.get(url)
        assert res.status_code == 401

    def test_crear_wod_for_time(self, client_autenticado):
        """Se puede registrar un WOD de tipo for_time con tiempo."""
        url = reverse("wod-list-create")
        res = client_autenticado.post(
            url,
            {
                "nombre_ejercicio": "Murph",
                "tipo": "for_time",
                "resultado_tiempo": 45.0,
            },
            format="json",
        )
        assert res.status_code == 201
        assert res.data["nombre_ejercicio"] == "Murph"

    def test_crear_wod_for_time_sin_tiempo(self, client_autenticado):
        """Un WOD for_time sin tiempo devuelve 400."""
        url = reverse("wod-list-create")
        res = client_autenticado.post(
            url,
            {
                "nombre_ejercicio": "Fran",
                "tipo": "for_time",
            },
            format="json",
        )
        assert res.status_code == 400

    def test_crear_wod_amrap_sin_repeticiones(self, client_autenticado):
        """Un WOD AMRAP sin repeticiones devuelve 400."""
        url = reverse("wod-list-create")
        res = client_autenticado.post(
            url,
            {
                "nombre_ejercicio": "Cindy",
                "tipo": "amrap",
            },
            format="json",
        )
        assert res.status_code == 400

    def test_aislamiento_datos(self, client, db):
        """Un atleta no puede ver los WODs de otro atleta."""
        # Creamos segundo usuario
        user2 = User.objects.create_user(
            username="user2",
            email="user2@gmail.com",
            password="Test1234!",
        )
        Wod.objects.create(
            usuario=user2,
            nombre_ejercicio="WOD de user2",
            tipo="for_time",
            resultado_tiempo=10.0,
        )

        # Nos autenticamos como user1
        url_token = reverse("token_obtain_pair")
        res_token = client.post(
            url_token,
            {
                "email": "user2@gmail.com",
                "password": "Test1234!",
            },
            format="json",
        )
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {res_token.data['access']}")

        url = reverse("wod-list-create")
        res = client.get(url)
        assert res.status_code == 200
        assert len(res.data["wods"]) == 1
        assert res.data["wods"][0]["nombre_ejercicio"] == "WOD de user2"


@pytest.mark.django_db
class TestWodDetail:
    """Tests del endpoint de detalle, edición y eliminación de WODs."""

    def test_ver_detalle_wod(self, client_autenticado, wod_creado):
        """El atleta puede ver el detalle de su WOD."""
        url = reverse("wod-detail", kwargs={"pk": wod_creado.id})
        res = client_autenticado.get(url)
        assert res.status_code == 200
        assert res.data["nombre_ejercicio"] == "Fran"
        assert res.data["notas"] == "Test WOD"

    def test_editar_wod(self, client_autenticado, wod_creado):
        """El atleta puede editar su WOD."""
        url = reverse("wod-detail", kwargs={"pk": wod_creado.id})
        res = client_autenticado.put(
            url,
            {
                "nombre_ejercicio": "Fran editado",
                "tipo": "for_time",
                "resultado_tiempo": 10.0,
            },
            format="json",
        )
        assert res.status_code == 200
        assert res.data["nombre_ejercicio"] == "Fran editado"

    def test_eliminar_wod(self, client_autenticado, wod_creado):
        """El atleta puede eliminar su WOD."""
        url = reverse("wod-detail", kwargs={"pk": wod_creado.id})
        res = client_autenticado.delete(url)
        assert res.status_code == 204
        assert Wod.objects.filter(id=wod_creado.id).count() == 0
