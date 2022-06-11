from django.urls import path
from .views import RegistrUserView, UserList

urlpatterns = [
    path('create', RegistrUserView.as_view(), name='registr'),
    path('list', UserList.as_view(), name='list')
]
