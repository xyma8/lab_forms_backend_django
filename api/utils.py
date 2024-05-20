from rest_framework.response import Response
from rest_framework import status
from .models import User


def get_user_from_token(request):
    token = request.headers.get('TokenAuth')

    if not token:
        return Response({'error': 'Токен не предоставлен'}, status=status.HTTP_400_BAD_REQUEST), None

    try:
        user = User.objects.get(token=token)
    except User.DoesNotExist:
        return Response({'error': 'Неверный токен'}, status=status.HTTP_401_UNAUTHORIZED), None

    return None, user