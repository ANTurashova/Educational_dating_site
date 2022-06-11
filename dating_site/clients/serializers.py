from rest_framework import serializers

from .models import User


def validate_passwords_similar(pass1, pass2, message='Пароли не совпадают!'):
    if pass1 != pass2:
        raise serializers.ValidationError(message)


def validate_letters(check_str, message='Стока может содержать только буквы!'):
    if not (check_str.isalpha()):
        raise serializers.ValidationError(message)


class UserRegistrSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField()

    class Meta:
        """Настройка полей"""
        model = User
        fields = ['email', 'first_name', 'last_name', 'sex', 'password', 'password2', 'avatar']

    def save(self, *args, **kwargs):
        """Метод для сохранения нового пользователя"""
        user = User(email=self.validated_data['email'])
        user.sex = self.validated_data['sex']
        validate_letters(self.validated_data['first_name'], 'Имя должно содержать только буквы!')
        validate_letters(self.validated_data['last_name'], 'Фамилия должна содержать только буквы!')
        user.first_name = self.validated_data['first_name']
        user.last_name = self.validated_data['last_name']
        user.avatar = self.validated_data['avatar']

        """Проверка пароля на валидность:"""
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        validate_passwords_similar(password, password2)

        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        """Поля, которые будем использовать"""
        model = User
        fields = ['id', 'first_name', 'last_name', 'sex', 'avatar', 'liked_list']
