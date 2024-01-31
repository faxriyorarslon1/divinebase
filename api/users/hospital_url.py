from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.users.views.hospital import HospitalModelViewSet
from api.users.views.hospital_vizit_qoldiq import HospitalVizitModelViewSet
from api.users.views.pharmacy import PharmacyModelViewSet

router = DefaultRouter()
router.register("hospital", HospitalModelViewSet)
router.register("pharmacy", PharmacyModelViewSet)
router.register('hospital_vizit_residue', HospitalVizitModelViewSet)
urlpatterns = [
    path("", include(router.urls))
]
