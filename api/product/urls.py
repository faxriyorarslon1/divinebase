from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.product.views import ProductApiModelViewSet, ProductWebModelApiViewSet

router = DefaultRouter()
router.register("product", ProductApiModelViewSet)
router.register('web_product', ProductWebModelApiViewSet)
urlpatterns = [
    path("", include(router.urls))
]
