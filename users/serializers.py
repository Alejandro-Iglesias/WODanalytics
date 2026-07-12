from rest_framework import serializers
from django.contrib.auth import get_user_model
import re
from rest_framework.validators import UniqueValidator

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    # Forzamos que el password sea estrictamente de entrada (nunca se enviará en un GET)
    password = serializers.CharField(write_only=True, style={"input_type": "password"})
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="Ya existe un usuario con este correo electrónico.",
            )
        ]
    )

    class Meta:
        model = User
        # Definimos los campos que aceptará el endpoint de registro
        fields = [
            "id",
            "username",
            "email",
            "password",
            "fecha_nacimiento",
            "peso_kg",
            "altura_cm",
        ]

    def validate_password(self, value):
        """
        Validamos que la contraseña cumpla los requisitos mínimos de seguridad
        usando expresiones regulares.
        """

        if len(value) < 8:
            raise serializers.ValidationError(
                "La contraseña debe tener al menos 8 caracteres."
            )
        if not re.search(r"[A-Z]", value):
            raise serializers.ValidationError(
                "La contraseña debe contener al menos una mayúscula."
            )
        if not re.search(r"[a-z]", value):
            raise serializers.ValidationError(
                "La contraseña debe contener al menos una minúscula."
            )
        if not re.search(r"\d", value):
            raise serializers.ValidationError(
                "La contraseña debe contener al menos un número."
            )
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise serializers.ValidationError(
                "La contraseña debe contener al menos un carácter especial."
            )
        return value

    def create(self, validated_data):
        """
        Sobrescribimos el método de creación para interceptar la contraseña
        y encriptarla antes de que impacte en PostgreSQL.
        """
        # Normalizamos el email a minúsculas para evitar duplicados
        validated_data["email"] = validated_data["email"].lower()
        # Extraemos el password en texto plano de los datos validados
        password = validated_data.pop("password")
        # Creamos la instancia del usuario con el resto de campos (username, email, etc.)
        user = User(**validated_data)
        user.set_password(password)
        # Guardamos el registro definitivo en la base de datos
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    # La fecha de registro (date_joined en Django) la marcamos como solo lectura
    fecha_registro = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        # Exponemos los datos del atleta, omitiendo el password por completo
        fields = [
            "id",
            "username",
            "email",
            "fecha_nacimiento",
            "peso_kg",
            "altura_cm",
            "fecha_registro",
        ]

        read_only_fields = [
            "id",
            "username",
            "email",
            "fecha_nacimiento",
            "peso_kg",
            "altura_cm",
            "fecha_registro",
        ]
