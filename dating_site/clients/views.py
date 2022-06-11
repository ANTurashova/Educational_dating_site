from django.conf import settings
from django.core.mail import send_mail
from geopy.distance import great_circle
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import User
from .serializers import UserRegistrSerializer, UserSerializer


def send_match_mails(user_list):
    for i in [0, 1]:
        safe_i = (i + 1) % 2
        arg1 = user_list[safe_i].first_name
        arg2 = user_list[safe_i].email
        message = "Вы понравились {0}! Почта участника: {1}".format(arg1, arg2)
        recipient = list()
        recipient.append(user_list[i].email)
        send_mail('Кажется, вы кому-то понравились...',
                  message,
                  settings.DEFAULT_FROM_EMAIL,
                  recipient,
                  fail_silently=False)


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


class UserListView(ListAPIView):
    """API endpoint, которая представляет собой список пользователей"""
    serializer_class = UserSerializer
    paginate_by = 10
    permission_classes = [AllowAny]

    def filter_queryset1(self, request, queryset):
        alluser = queryset.exclude(id=self.request.user.id)
        exclude_e = alluser
        distparam = request.GET.get('distance')
        if distparam:
            for user in alluser:
                from_loc = (self.request.user.latitude, self.request.user.latitude)
                self_loc = (user.latitude, user.longitude)
                distance = great_circle(from_loc, self_loc).km
                if distance > float(distparam):
                    exclude_e = exclude_e.exclude(id=user.id)
        return exclude_e

    def get_queryset(self):
        """Фильтрует queryset по значениям из get запроса"""
        keys = ['first_name', 'last_name', 'sex']
        filters = {}
        req = self.request
        for key in keys:
            filter = req.query_params.getlist(key)
            if filter:
                filters['{}__in'.format(key)] = filter
        queryset = User.objects.all()
        if req.GET.get('distance') and req.user.is_authenticated:
            queryset = self.filter_queryset1(req, queryset)
        return queryset.filter(**filters)


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def UserMatchView(request, pk):
    if pk == request.user.id:
        data = dict()
        data['1'] = "Вы не можете отправить симпатию себе"
        return Response(data, status=status.HTTP_200_OK)
    user = User.objects.get(id=request.user.id)
    own_liked_list = user.liked_list
    liked_user = User.objects.filter(id=pk)

    if liked_user:
        liked_user = User.objects.get(id=pk)
        if not (pk in own_liked_list):
            own_liked_list.append(pk)
            user.liked_list = own_liked_list
            user.save(update_fields=['liked_list'])

    data = {}
    if liked_user:
        liked_user_list = liked_user.liked_list
        if user.id in liked_user_list:
            st = "Это взаимная симпатия! Его/её электронная почта: "
            data['1'] = st + liked_user.email
            send_match_mails([user, liked_user])
            return Response(data, status=status.HTTP_200_OK)
    else:
        data['1'] = "Пользователь не найден"
    return Response(data, status=status.HTTP_200_OK)
