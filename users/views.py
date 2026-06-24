from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from .serializers import UserProfileSerializer, UserRegistrationSerializer


class RegisterView(APIView):
    """
    Endpoint público para el registro de nuevos atletas.
    No requiere autenticación — cualquiera puede registrarse.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        # Pasamos los datos que vienen del frontend al serializer para validarlos

        serializer = UserRegistrationSerializer(data=request.data)
        # erializer — hashea la contraseña y guarda en PostgreSQL
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                UserRegistrationSerializer(user).data,
                status=status.HTTP_201_CREATED,
            )
        # Si los datos no son válidos devolvemos los errores de validación
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """
    Endpoint protegido que devuelve el perfil del atleta autenticado.
    Requiere token JWT válido en el header de la petición.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        # request.user es el usuario autenticado — DRF lo extrae
        # automáticamente del token JWT que viene en el header
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
