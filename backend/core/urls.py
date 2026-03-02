from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import path, include
from kanban import views
router = DefaultRouter()
router.register(r'tasks', views.TaskViewSet)
router.register(r'teams', views.TeamViewSet)
router.register(r'memberships', views.MembershipViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/', include(router.urls)),
]

