from django.db import models

from users.models import User


# Create your models here.
class Habbit(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    place = models.CharField(
        "Место выполнения привычки", max_length=50, blank=True, null=True
    )
    time = models.TimeField("Время выполнения привычки")
    action = models.CharField("Действие", max_length=50)
    is_enjoyable = models.BooleanField(
        "Признак приятной привычки", default=False, blank=True, null=True
    )
    related_habbit = models.ForeignKey(
        "self", on_delete=models.SET_NULL, blank=True, null=True
    )
    periodicity = models.PositiveIntegerField(
        "Периодичность привычки", help_text="Периодичность в днях"
    )
    reward = models.CharField("Награда", max_length=50, blank=True, null=True)
    time_to_complete = models.PositiveIntegerField("Время на выполнение")
    is_public = models.BooleanField(
        "Признак публичности", default=False, blank=True, null=True
    )

    def __str__(self):
        return f"я буду {self.action} в {self.time} в {self.place}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
