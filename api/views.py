from django.conf import settings
from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer, UserDataSerializer, AuthSerializer, UserThemeSerializer
from rest_framework.response import Response
from rest_framework import status
import requests

from .utils import get_user_from_token


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserSignup(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # Это вызовет метод save() модели, который сгенерирует токен
            return Response({'id': user.id, 'token': user.token}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    def post(self, request):
        serializer = AuthSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            return Response({'id': user.id, 'token': user.token}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUserDataByToken(APIView):
    def get(self, request):
        token = request.headers.get('TokenAuth')

        if not token:
            return Response({'error': 'Токен не предоставлен'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(token=token)
        except User.DoesNotExist:
            return Response({'error': 'Неверный токен'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = UserDataSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetUserTheme(APIView):
    def get(self, request):
        response, user = get_user_from_token(request)
        if response:
            return response

        serializer = UserThemeSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChangeUserTheme(APIView):
    def get(self, request):
        response, user = get_user_from_token(request)
        if response:
            return response

        try:
            # Переключаем значение darktheme
            user.darktheme = not user.darktheme
            user.save()
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserThemeSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReCaptchaVerification(APIView):
    def get(self, request):
        token = request.headers.get('TokenAuth')

        if not token:
            return Response({'error': 'Токен reCAPTCHA не предоставлен'}, status=status.HTTP_400_BAD_REQUEST)

        response = requests.post('https://www.google.com/recaptcha/api/siteverify', {
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'response': token
        })

        if response.status_code == 200:
            data = response.json()
            if data['success']:
                return Response({'success': True}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Проверка reCAPTCHA не удалась'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Ошибка при запросе к сервису reCAPTCHA'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
