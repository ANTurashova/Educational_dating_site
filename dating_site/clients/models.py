from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


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
    is_staff = models.BooleanField(default=False)  # Статус админа

    def user_directory_path(instance, filename):
        """Путь, куда будет осуществлена загрузка: MEDIA_ROOT/user_<id>_<filename>"""
        return 'images/user_{0}_{1}'.format(instance.id, filename)

    avatar = models.ImageField(verbose_name="Avatar", null=True, blank=True, upload_to=user_directory_path)
    Male = 'M'
    Female = 'F'
    sex_Choices = ((Male, 'Male'), (Female, 'Female'),)
    Sex = models.CharField(
        max_length=1,
        choices=sex_Choices,
        default=Female,
        help_text="Enter your gender",
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = MyUserManager()

    def __str__(self):
        """Метод для отображения в админ панели"""
        return self.email

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_full_name(self):
        return '{0} {1}'.format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name
