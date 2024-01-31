"""DivineBase URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_swagger.views import get_swagger_view

from DivineBase import settings
from DivineBase.views import configs

schema_view = get_swagger_view(title='Pastebin API')

API_TITLE = 'Distributive'
API_DESCRIPTION = 'Agent Manager'
yasg_schema_view = get_schema_view(
    openapi.Info(
        title="Distributive API",
        default_version='version1.0',
        description="Distributive API documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="dilshodzokirov03@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    # renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer],
    public=True,
    permission_classes=(permissions.AllowAny,),
)
version = 'version1'
urlpatterns = [
    path('swagger/', yasg_schema_view.with_ui('swagger',
                                              cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', yasg_schema_view.with_ui('redoc',
                                            cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path(f"{version}/users/", include('api.users.urls')),
    path(f"{version}/product/", include("api.product.urls")),
    path(f"{version}/order/", include("api.order.urls")),
    path(f"{version}/hospital/", include('api.users.hospital_url')),
    path(f'{version}/index', configs, name='index'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
