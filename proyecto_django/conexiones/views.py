from django.shortcuts import render
from django.http import JsonResponse
from .models import Organismo, Medida
from .serializers import OrganismoSerializer, MedidaSerializer
from rest_framework import generics
from drf_spectacular.utils import extend_schema



# Bienvenida
# TODO: Cambiar a una vista de bienvenida mas elaborada con los miembros del equipo
@extend_schema(
    summary="Bienvenida",
    description="Mensaje de prueba para comprobar que la API está activa.",
    methods=["GET"]
)
def bienvenida(request):
    '''
    Una amistosa bienvenida.
    '''
    return JsonResponse({"mensaje": "¡Bienvenido!"})


# Listar Organismos
@extend_schema(
    summary="Listar organismos",
    description="Devuelve una lista con todos los organismos registrados en el sistema.",
    methods=["GET"],
    responses=OrganismoSerializer(many=True)
)
def listar_organismos(request):
    '''
    API que devuelve una lista de los organismos:

    Métodos:
    - 'GET /listar_organismos/': Lista todos los organismos involucrados en el PPDA
    '''
    organismos = Organismo.objects.all().values("id_organismo", "nombre", "region")
    return JsonResponse(list(organismos), safe=False)


# Buscar Organismos
# Busca con el formato /buscar_organismos/nombre_a_buscar/
@extend_schema(
    summary="Buscar organismos por nombre",
    description="Busca organismos cuyo nombre coincida parcialmente con el parámetro de búsqueda.",
    responses=OrganismoSerializer(many=True)
)
class BuscarOrganismos(generics.ListAPIView):
    '''
    API que devuelve una lista de los organismos:

    Métodos:
    - 'GET /BuscarOrganismos/{nombre del  organismo}': Devuelve el organismo, su id y región asociada.
    '''
    serializer_class = OrganismoSerializer

    def get_queryset(self):
        query = self.kwargs.get('query', '')
        return Organismo.objects.filter(nombre__icontains=query)


# Crear Organismos
@extend_schema(
    summary="Crear un nuevo organismo",
    description="Permite registrar un nuevo organismo proporcionando su nombre y región.",
    request=OrganismoSerializer,
    responses=OrganismoSerializer
)
class CrearOrganismo(generics.CreateAPIView):
    '''
    devuelve una lista de los organismos:

    Métodos:
    - 'POST /CrearOrganismo/{Nombre del nuevo organismo}': Crea un nuevo organismo en la tabla de Organismos.
    '''
    queryset = Organismo.objects.all()
    serializer_class = OrganismoSerializer


# Mostrar Medidas
@extend_schema(
    summary="Mostrar medidas por organismo",
    description="Devuelve una lista de medidas asociadas al nombre del organismo proporcionado.",
    responses=MedidaSerializer(many=True)
)
class MostrarMedidas(generics.ListAPIView):
    '''
    devuelve una lista de las medidas:

    Métodos:
    - 'GET /MostrarMedidas/{id_medida}': Muestra las medidas asociadas a un organismo.
    '''
    serializer_class = MedidaSerializer

    def get_queryset(self):
        query = self.kwargs.get('query', '')
        return Medida.objects.filter(organismo__nombre__icontains=query)
