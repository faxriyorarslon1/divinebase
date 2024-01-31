from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.order.views import OrderModelViewSet, CompanyModelViewSet, CompanyWebModelViewSet, WebOrderModelViewSet
from api.order.views.contract_number import ContractNumberModelViewSet

router = DefaultRouter()
router.register("order", OrderModelViewSet)
router.register('company', CompanyModelViewSet)
router.register('web_company', CompanyWebModelViewSet)
router.register("web_order", WebOrderModelViewSet)
router.register('contract_number', ContractNumberModelViewSet)
urlpatterns = [
    path("", include(router.urls))
]
