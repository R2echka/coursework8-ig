from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    username = models.CharField(
        "Имя пользователя", max_length=20, blank=True, null=True
    )
    email = models.EmailField(unique=True, verbose_name="Email")
    tg_id = models.CharField("id тг чата", max_length=50, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
