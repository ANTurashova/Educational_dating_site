from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from .models import User
from .serializers import UserRegistrSerializer, UserSerializer


class RegistrUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """Метод для создания нового пользователя"""
        serializer = UserRegistrSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = True
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = serializer.errors
            return Response(data)


class UserList(ListAPIView):
    """API endpoint, которая представляет собой список пользователей"""
    queryset = User.objects.all()
    # serializer_class = UserRegistrSerializer
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
