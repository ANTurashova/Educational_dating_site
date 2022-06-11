from django.urls import path
from .views import RegistrUserView, UserListView, UserMatchView

urlpatterns = [
    path('create', RegistrUserView.as_view(), name='registr'),
    path('list', UserListView.as_view(), name='list'),
    path('<int:pk>/match/', UserMatchView, name='match'),
]
