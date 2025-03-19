from rest_framework.routers import DefaultRouter

from habbits.apps import HabbitsConfig
from habbits.views import HabbitViewSet

app_name = HabbitsConfig.name
router = DefaultRouter()
router.register(r"habbit", HabbitViewSet, basename="habbit")

urlpatterns = [] + router.urls
