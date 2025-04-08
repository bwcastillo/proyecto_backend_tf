from django.urls import path
from .views import (
    bienvenida,
    listar_organismos,
    BuscarOrganismos,
    CrearOrganismo,
    MostrarMedidas
)

urlpatterns = [
    # Vista de bienvenida
    path('bienvenida/', bienvenida, name='bienvenida'),

    # Organismos
    path('organismos/', listar_organismos, name='listar_organismos'),
    path('crear_organismo/', CrearOrganismo.as_view(), name='crear_organismo'),
    path('buscar_organismos/<str:query>/', BuscarOrganismos.as_view(), name='buscar_organismos'),

    # Medidas
    path('mostrar_medidas/<str:query>/', MostrarMedidas.as_view(), name='mostrar_medidas'),
]
