import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def client():
    """Cliente de la API para hacer peticiones en los tests."""
    return APIClient()


@pytest.fixture
def usuario_registrado(db):
    """Crea un usuario de prueba en la base de datos."""
    user = User.objects.create_user(
        username="testuser",
        email="test@gmail.com",
        password="Test1234!",
    )
    return user


@pytest.fixture
def token_autenticado(client, usuario_registrado):
    """Obtiene un token JWT para el usuario de prueba."""
    url = reverse("token_obtain_pair")
    res = client.post(
        url,
        {
            "email": "test@gmail.com",
            "password": "Test1234!",
        },
        format="json",
    )
    return res.data["access"]


@pytest.mark.django_db
class TestRegistro:
    """Tests del endpoint de registro de usuarios."""

    def test_registro_exitoso(self, client):
        """Un usuario puede registrarse con datos válidos."""
        url = reverse("register")
        res = client.post(
            url,
            {
                "username": "nuevo",
                "email": "nuevo@gmail.com",
                "password": "Test1234!",
            },
            format="json",
        )
        assert res.status_code == 201
        assert res.data["email"] == "nuevo@gmail.com"
        assert "password" not in res.data

    def test_registro_password_debil(self, client):
        """El registro falla si la contraseña no cumple los requisitos."""
        url = reverse("register")
        res = client.post(
            url,
            {
                "username": "nuevo",
                "email": "nuevo@gmail.com",
                "password": "1234",
            },
            format="json",
        )
        assert res.status_code == 400
        assert "password" in res.data

    def test_registro_email_duplicado(self, client, usuario_registrado):
        """El registro falla si el email ya existe."""
        url = reverse("register")
        res = client.post(
            url,
            {
                "username": "otro",
                "email": "test@gmail.com",
                "password": "Test1234!",
            },
            format="json",
        )
        assert res.status_code == 400

    def test_registro_normaliza_email(self, client):
        """El email se guarda siempre en minúsculas."""
        url = reverse("register")
        res = client.post(
            url,
            {
                "username": "nuevo",
                "email": "NUEVO@GMAIL.COM",
                "password": "Test1234!",
            },
            format="json",
        )
        assert res.status_code == 201
        assert res.data["email"] == "nuevo@gmail.com"


@pytest.mark.django_db
class TestLogin:
    """Tests del endpoint de login JWT."""

    def test_login_correcto(self, client, usuario_registrado):
        """El login devuelve access y refresh token."""
        url = reverse("token_obtain_pair")
        res = client.post(
            url,
            {
                "email": "test@gmail.com",
                "password": "Test1234!",
            },
            format="json",
        )
        assert res.status_code == 200
        assert "access" in res.data
        assert "refresh" in res.data

    def test_login_password_incorrecta(self, client, usuario_registrado):
        """El login falla con contraseña incorrecta."""
        url = reverse("token_obtain_pair")
        res = client.post(
            url,
            {
                "email": "test@gmail.com",
                "password": "wrongpass",
            },
            format="json",
        )
        assert res.status_code == 401


@pytest.mark.django_db
class TestPerfil:
    """Tests del endpoint de perfil de usuario."""

    def test_perfil_con_token(self, client, token_autenticado):
        """El perfil devuelve los datos del usuario autenticado."""
        url = reverse("profile")
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token_autenticado}")
        res = client.get(url)
        assert res.status_code == 200
        assert res.data["email"] == "test@gmail.com"

    def test_perfil_sin_token(self, client):
        """El perfil devuelve 401 sin token."""
        url = reverse("profile")
        res = client.get(url)
        assert res.status_code == 401
