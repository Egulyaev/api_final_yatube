from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework_simplejwt import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    path(
        'api/v1/token/',
        views.TokenObtainPairView.as_view(),
        name="jwt-create"
    ),
    path(
        'api/v1/token/refresh/',
        views.TokenRefreshView.as_view(),
        name="jwt-refresh"
    ),
]
