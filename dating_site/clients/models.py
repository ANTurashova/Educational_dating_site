from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from .watermark import watermark
import json


def watermarkImage(image_file):
    """Обертка для накладывания вотермарки. Принимает File, возвращает файл BytesIO"""
    mark = 'images/watermark/watermark.png'
    return watermark(image_file, mark, 'scale', 0.45)


class MyUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Метод для создания пользователя"""
        if not email:
            raise ValueError("Вы не ввели Email")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password):
        """Метод для создания обычного пользователя"""
        return self._create_user(email, password)

    def create_superuser(self, email, password):
        """Метод для создания админа сайта"""
        return self._create_user(email, password, is_staff=True, is_superuser=True)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_staff = models.BooleanField(default=False)
    liked_list = models.TextField(blank=True, default="[-1, -2]")

    def user_directory_path(instance, filename):
        """Путь, куда будет осуществлена загрузка: MEDIA_ROOT/user_<email>_<filename>"""
        return 'images/user_{0}_{1}'.format(instance.email, filename)

    avatar = models.ImageField(verbose_name="Avatar", null=True, blank=True, upload_to=user_directory_path)
    Male = 'M'
    Female = 'F'
    sex_Choices = (
        (Male, 'Male'),
        (Female, 'Female'),
    )
    sex = models.CharField(
        max_length=1,
        choices=sex_Choices,
        default=Female,
        help_text="Введите свой пол",
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = MyUserManager()

    def __str__(self):
        """Метод для отображения в админ панели"""
        return self.email

    def save(self, *args, **kwargs):
        """Метод для сохранения аватарки с наложенной вотермаркой"""
        if self.avatar:
            self.avatar = watermarkImage(self.avatar.file)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_full_name(self):
        return '{0} {1}'.format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name

    def set_liked_list(self, x):
        self.liked_list = json.dumps(x)

    def get_liked_list(self):
        return json.loads(self.liked_list)
