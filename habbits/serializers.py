from rest_framework import serializers
from rest_framework.serializers import ValidationError

from habbits.models import Habbit


class HabbitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habbit
        fields = "__all__"

    def validate(self, data):
        if "time_to_complete" in data and data["time_to_complete"] > 120:
            raise ValidationError("Время выполнения должно быть не больше 120 секунд")
        elif "related_habbit" in data and not (data["is_enjoyable"]):
            raise ValidationError("Связанная привычка должна быть приятной")
        elif data["is_enjoyable"] and ("reward" in data or "related_habbit" in data):
            raise ValidationError(
                "У приятной привычки не может быть вознаграждения или связанной привычки"
            )
        elif (
            "periodicity" in data
            and data["periodicity"] is not None
            and data["periodicity"] > 7
        ):
            raise ValidationError("Нельзя ставить периодичность больше 7 дней")
        return data
