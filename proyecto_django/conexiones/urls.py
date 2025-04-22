from django.urls import path
from .views import (
    BienvenidaRootView,
    listar_organismos,
    BuscarOrganismos,
    CrearOrganismo,
    MostrarMedidas,
    ReadmeHTMLView,
    ChangelogHTMLView,
    LogPlainTextView
)

urlpatterns = [
    # Vista de bienvenida
    path('', BienvenidaRootView.as_view(), name='bienvenida-root'),

    # Organismos
    path('organismos/', listar_organismos, name='listar_organismos'),
    path('crear_organismo/', CrearOrganismo.as_view(), name='crear_organismo'),
    path('buscar_organismos/<str:query>/',
         BuscarOrganismos.as_view(), name='buscar_organismos'),

    # Medidas
    path('mostrar_medidas/<str:query>/',
         MostrarMedidas.as_view(), name='mostrar_medidas'),

    # Endpoint para la documentación de la APIs
    path('docs/readme-html/', ReadmeHTMLView.as_view(), name='readme-html'),
    path('docs/changelog-html/', ChangelogHTMLView.as_view(), name='readme-html'),

    # Endpoint de los LOGS de la API
    path('logs/texto/', LogPlainTextView.as_view(), name='log-texto'),

]
