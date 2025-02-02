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
        if query:
            return Organismo.objects.filter(nombre__icontains=query)
        return Organismo.objects.all()


# Crear Organismos
class CrearOrganismo(generics.CreateAPIView):
    queryset = Organismo.objects.all()
    serializer_class = OrganismoSerializer


# Mostrar Medidas
# Muestra segun busqueda por el id del organismo, por ahora...
# TODO: cambiar busqueda por ir a nombre del organismo
# TODO: Mostrar el nombre del organismo en lugar del id
class MostrarMedidas(generics.ListAPIView):
    # queryset = Medida.objects.all()
    serializer_class = MedidaSerializer

    def get_queryset(self):
        query = self.kwargs.get('query', '')
        if query:
            return Medida.objects.filter(id_organismo__icontains=query)
        return Medida.objects.all()
