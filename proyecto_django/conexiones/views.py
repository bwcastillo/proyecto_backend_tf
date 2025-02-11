from django.shortcuts import render
from django.http import JsonResponse
from .models import Organismo, Medida
from .serializers import OrganismoSerializer, MedidaSerializer
from rest_framework import generics


# Bienvenida
# TODO: Cambiar a una vista de bienvenida mas elaborada con los miembros del equipo
def bienvenida(request):
    return JsonResponse({"mensaje": "¡Bienvenido!"})


# Listar Organismos
def listar_organismos(request):
    organismos = Organismo.objects.all().values(
        "id_organismo", "nombre", "region")
    return JsonResponse(list(organismos), safe=False)


# Buscar Organismos
# Busca con el formato /buscar_organismos/nombre_a_buscar/
class BuscarOrganismos(generics.ListAPIView):
    serializer_class = OrganismoSerializer

    def get_queryset(self):
        query = self.kwargs.get('query', '')
        organismos = Organismo.objects.all().values("id_organismo", "nombre")
        #match query name with id_organismo
        organismo_id = organismos.filter(nombre__icontains=query)
        if organismo_id:
            return Organismo.objects.filter(id_organismo__icontains=organismo_id[0]['id_organismo'])


# Crear Organismos
class CrearOrganismo(generics.CreateAPIView):
    queryset = Organismo.objects.all()
    serializer_class = OrganismoSerializer


# Mostrar Medidas
class MostrarMedidas(generics.ListAPIView):
    serializer_class = MedidaSerializer

    def get_queryset(self):
        query = self.kwargs.get('query', '')
        organismos = Organismo.objects.all().values("id_organismo", "nombre")
        #match query name with id_organismo
        organismo_id = organismos.filter(nombre__icontains=query)
        if organismo_id:
            return Medida.objects.filter(id_organismo__icontains=organismo_id[0]['id_organismo'])
