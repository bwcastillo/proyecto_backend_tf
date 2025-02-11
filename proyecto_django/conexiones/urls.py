from django.urls import path
from .views import bienvenida, listar_organismos, BuscarOrganismos, CrearOrganismo, MostrarMedidas

urlpatterns = [
    path('bienvenida/', bienvenida, name='bienvenida'),
    path('organismos/', listar_organismos, name='listar_organismos'),
    path('buscar_organismos/', BuscarOrganismos.as_view(),
         name='buscar_organismos'),
    path('buscar_organismos/<str:query>/',
         BuscarOrganismos.as_view(), name='buscar_organismos'),
    path('crear_organismo/', CrearOrganismo.as_view(), name='crear_organismo'),
    path('mostrar_medidas/<str:query>/',
         MostrarMedidas.as_view(), name='mostrar_medidas'),
]
