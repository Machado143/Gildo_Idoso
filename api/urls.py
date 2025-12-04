from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'idosos', IdosoViewSet)
router.register(r'dispositivos', DispositivoViewSet)
router.register(r'dados-saude', DadoSaudeViewSet)
router.register(r'alertas', AlertaViewSet)
router.register(r'historico', HistoricoSaudeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('docs/', api_docs, name='api-docs'),
    path('welcome/', api_welcome, name='api_welcome'),
    path('alertas/emergencia/', api_alertas_emergencia, name='api_alertas_emergencia'),
]
