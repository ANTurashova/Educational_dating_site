from django.urls import path
from .views import RegistrUserView

urlpatterns = [
    path('create', RegistrUserView.as_view(), name='registr')
]
