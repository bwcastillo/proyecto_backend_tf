from django.shortcuts import render
from django.http import JsonResponse
from .models import Organismo, Medida
from .serializers import OrganismoSerializer, MedidaSerializer
from rest_framework import generics


# Bienvenida
# TODO: Cambiar a una vista de bienvenida mas elaborada con los miembros del equipo
def bienvenida(request):
    '''
    Una amistosa bienvenida.
    '''
    return JsonResponse({"mensaje": "¡Bienvenido!"})


# Listar Organismos
def listar_organismos(request):
    '''
    API que devuelve una lista de los organismos:

    Métodos:
    - 'GET /listar_organismos/': Lista todos los organismos involucrados en el PPDA
    '''

    organismos = Organismo.objects.all().values(
        "id_organismo", "nombre", "region")
    return JsonResponse(list(organismos), safe=False)


# Buscar Organismos
# Busca con el formato /buscar_organismos/nombre_a_buscar/
class BuscarOrganismos(generics.ListAPIView):
    '''
    API que devuelve una lista de los organismos:

    Métodos:
    - 'GET /BuscarOrganismos/{nombre del  organismo}': Devuelve el organismo, su id y región asociada.
    '''


    serializer_class = OrganismoSerializer

    def get_queryset(self): #Bryan: CONSIDERAR QUE DEVUELVA MÁS TABLAS ASOCIADAS AL ORGANISMO
        query = self.kwargs.get('query', '')
        organismos = Organismo.objects.all().values("id_organismo", "nombre")
        #match query name with id_organismo
        organismo_id = organismos.filter(nombre__icontains=query)
        if organismo_id:
            return Organismo.objects.filter(id_organismo__icontains=organismo_id[0]['id_organismo'])


# Crear Organismos
class CrearOrganismo(generics.CreateAPIView):
    '''
    API que devuelve una lista de los organismos:

    Métodos:
    - 'POST /CrearOrganismo/{Nombre del nuevo organismo}': Crea un nuevo organismo en la tabla de Organismos.
    '''

    queryset = Organismo.objects.all()
    serializer_class = OrganismoSerializer


# Mostrar Medidas
class MostrarMedidas(generics.ListAPIView):
    serializer_class = MedidaSerializer
    '''
    API que devuelve una lista de los organismos:

    Métodos:
    - 'GET /MostrarMedidas/{id_medida}': Crea un nuevo organismo en la tabla de Organismos.
    '''
    def get_queryset(self):
        query = self.kwargs.get('query', '')
        organismos = Organismo.objects.all().values("id_organismo", "nombre")
        #match query name with id_organismo
        organismo_id = organismos.filter(nombre__icontains=query)
        if organismo_id:
            return Medida.objects.filter(id_organismo__icontains=organismo_id[0]['id_organismo'])
