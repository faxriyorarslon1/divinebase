from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views.check_mp import CheckMpModelViewSet
from .views.city import CityModelViewSet
from .views.debit import DebitModelViewSet
from .views.doctor import DoctorModelViewSet
from .views.doctor_agreement import ModelDoctorAgreement
from .views.double_vizit_excel import DoubleVizitExcelModelViewSet
from .views.hospital_vizit_qoldiq import HospitalVizitExcelViewSet
from .views.income import IncomeModelViewSet
from .views.location import LocationModelViewSet
from .views.mobile_location import MobileLocationModelViewSet
from .views.order_excel_lists import OrderExcelModelViewSet, DownloadView
from .views.registration_views import RegistrationModelViewSet, VillageModelApiViewSet, UserModelViewSet
from .views.version_view import VersionModelApiViewSet, MobileAPIView
from .views.vizit import VizitCreateAPI, VizitExcelApi

router = DefaultRouter()
router.register("registration", RegistrationModelViewSet)
router.register("district", VillageModelApiViewSet)
router.register("user", UserModelViewSet)
router.register("location", LocationModelViewSet)
router.register("mobile_location", MobileLocationModelViewSet)
router.register("city", CityModelViewSet)
router.register("agree_doctor", ModelDoctorAgreement)
router.register("doctor", DoctorModelViewSet)
router.register('order_excel', OrderExcelModelViewSet)
router.register('debit', DebitModelViewSet)
router.register('income', IncomeModelViewSet)
router.register('check_mp', CheckMpModelViewSet)
router.register('vizit', VizitCreateAPI)
router.register('version', VersionModelApiViewSet)
router.register('vizit_excel', VizitExcelApi)
router.register('double_vizit_excel', DoubleVizitExcelModelViewSet)
router.register('hospital_residue_excel', HospitalVizitExcelViewSet)
# router.register('mobile_app', MobileAPIView)


urlpatterns = [
    path('vizit_excel', DownloadView.as_view()),
    path('mobile_app', MobileAPIView.as_view()),
    path("", include(router.urls))
]
