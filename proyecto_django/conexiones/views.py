import os
import re
import markdown2
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import Organismo, Medida
from .serializers import OrganismoSerializer, MedidaSerializer

LOG_PATH = os.path.join(settings.BASE_DIR, 'logs', 'proyecto.log')


class MarkdownHtmlView(APIView):
    """
    Vista base para mostrar archivos Markdown (.md) como HTML estilizado y renderizado.
    Soporta:
    - Conversión de markdown a HTML con `markdown2`
    - Diagramas Mermaid convertidos a <div class="mermaid">
    - Tablas, bloques de código
    """

    permission_classes = [AllowAny]
    markdown_filename = None  # Debe ser definido por subclases

    def get(self, request):
        if not self.markdown_filename:
            return HttpResponse("<h1>Error: archivo Markdown no especificado.</h1>", status=500)

        root_path = os.path.dirname(settings.BASE_DIR)
        file_path = os.path.join(root_path, self.markdown_filename)

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content_md = f.read()

                # Reemplazar bloques mermaid por div.mermaid
                def replace_mermaid_blocks(match):
                    code = match.group(1)
                    return f'<div class="mermaid">\n{code}\n</div>'

                mermaid_pattern = r'```mermaid\s*\n([\s\S]*?)\n```'
                content_md = re.sub(
                    mermaid_pattern, replace_mermaid_blocks, content_md)

                # Convertir markdown a HTML
                html_content = markdown2.markdown(
                    content_md,
                    extras=["fenced-code-blocks", "tables",
                            "strike", "code-friendly"]
                )

                # HTML final con estilos y script Mermaid
                html = f"""
                <html>
                <head>
                    <meta charset="utf-8">
                    <title>{self.markdown_filename}</title>
                    <style>
                        body {{ font-family: sans-serif; padding: 2rem; max-width: 900px; margin: auto; }}
                        pre {{ background-color: #f4f4f4; padding: 1em; overflow-x: auto; }}
                        code {{ background-color: #eee; padding: 2px 4px; border-radius: 4px; }}
                        table {{ border-collapse: collapse; width: 100%; }}
                        th, td {{ border: 1px solid #ddd; padding: 8px; }}
                        th {{ background-color: #f2f2f2; }}
                    </style>
                    <script type="module">
                        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
                        mermaid.initialize({{ startOnLoad: true }});
                    </script>
                </head>
                <body>
                    {html_content}
                </body>
                </html>
                """
                return HttpResponse(html)
        except FileNotFoundError:
            return HttpResponse(f"<h1>{self.markdown_filename} no encontrado</h1>", status=404)


# Bienvenida
@extend_schema_view(
    get=extend_schema(
        summary="Bienvenida",
        description="Endpoint de bienvenida en la raíz del sistema.",
        tags=["Inicio"],
    ),
    exclude=True
)
class BienvenidaRootView(APIView):
    """
    Muestra una página HTML de bienvenida usando plantilla.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        integrantes = [
            "Geraldy Suarez",
            "Carol Leiva",
            "Scarlett Espinoza",
            "Bryan Castillo",
            "Nicolas Mardones",
            "Ulises Campodonico",
            "Manuel Denis"
        ]
        return render(request, 'bienvenida.html', {'integrantes': integrantes})


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


# Muestra el archivo README.md
@extend_schema(
    summary="Ver README.md",
    description="Devuelve el contenido del archivo README.md del proyecto.",
    exclude=True
)
class ReadmeHTMLView(MarkdownHtmlView):
    """
    Muestra el contenido de README.md como HTML enriquecido.
    """
    markdown_filename = "README.md"


# Muestra el archivo CHANGELOG.md
@extend_schema(
    summary="Ver CHANGELOG.md",
    description="Devuelve el contenido del archivo CHANGELOG.md del proyecto.",
    exclude=True
)
class ChangelogHTMLView(MarkdownHtmlView):
    """
    Muestra el contenido de CHANGELOG.md como HTML enriquecido.
    """
    markdown_filename = "CHANGELOG.md"


# Muestra los logs de la API
@extend_schema(
    summary="Ver logs del sistema",
    description="Retorna el contenido del archivo de logs como texto plano.",
    tags=["Logs"]
)
class LogPlainTextView(APIView):
    """
    Devuelve el log de Django como texto plano.
    Solo accesible para usuarios administradores.
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        if not os.path.exists(LOG_PATH):
            return HttpResponse("Archivo de log no encontrado.", status=404)

        with open(LOG_PATH, 'r', encoding='utf-8') as f:
            content = f.read()

        return HttpResponse(content, content_type="text/plain")
