from rest_framework import serializers
from .models import User
from .exceptions import ConflictException
from django.contrib.auth.hashers import check_password


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


class AuthSerializer(serializers.Serializer):
    login = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        login = data.get('login')
        password = data.get('password')
        user = User.objects.filter(login=login).first()

        if user is None:
            raise serializers.ValidationError('Неверный логин или пароль.')

        if not check_password(password, user.password):
            raise serializers.ValidationError('Неверный логин или пароль.')

        data['user'] = user
        return data


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['login', 'name']


class UserThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['darktheme']
