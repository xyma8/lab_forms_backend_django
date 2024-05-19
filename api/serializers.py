from rest_framework import serializers
from .models import User
from .exceptions import ConflictException


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "surname", "email", "login", "password", "gender"]

    def validate(self, data):
        email = data.get('email', None)
        login = data.get('login', None)

        if User.objects.filter(email=email).exists():
            raise ConflictException({'email': 'Пользователь с таким email уже существует.'})

        if User.objects.filter(login=login).exists():
            raise ConflictException({'login': 'Пользователь с таким логином уже существует.'})

        return data
