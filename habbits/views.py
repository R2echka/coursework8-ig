from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from habbits.models import Habbit
from habbits.paginators import CustomPaginator
from habbits.serializers import HabbitSerializer
from habbits.services import habbit_reminder
from users.permissions import Owner


# Create your views here.
class HabbitViewSet(viewsets.ModelViewSet):
    serializer_class = HabbitSerializer
    pagination_class = CustomPaginator
    queryset = Habbit.objects.all()

    def perform_create(self, serializer):
        habbit = serializer.save()
        habbit.owner = self.request.user
        habbit.save()
        habbit_reminder(habbit)

    @action(detail=False, methods=["GET"])
    def public_habbits(self, request):
        public_habbits = self.queryset.filter(is_public=True)
        serializer = self.get_serializer(public_habbits, many=True)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action not in ["create", "public_habbits"]:
            self.permission_classes = (Owner,)
        return super().get_permissions()
