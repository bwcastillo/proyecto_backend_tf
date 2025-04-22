from django.test import TestCase
from django.contrib.auth.models import User
from .models import Organismo, Medida, Reporte, Cumplimiento, PPDA, PeriodoPPDA, Indicador


class OrganismoModelTest(TestCase):
    """
    Pruebas unitarias para el modelo Organismo.
    """

    def test_creacion_organismo(self):
        """
        Verifica que se puede crear un Organismo correctamente.
        """
        organismo = Organismo.objects.create(
            nombre="Ministerio del Medio Ambiente", region="Valparaíso")
        self.assertEqual(str(organismo), "Ministerio del Medio Ambiente")


class MedidaModelTest(TestCase):
    """
    Pruebas unitarias para el modelo Medida.
    """

    def setUp(self):
        """
        Configura los datos necesarios antes de cada prueba.
        """
        self.organismo = Organismo.objects.create(nombre="SMA", region="RM")
        self.indicador = Indicador.objects.create(
            descripcion="Índice de emisiones",
            formula_calculo="(valor / total) * 100",
            medio_verificacion="Informe técnico"
        )
        self.medida = Medida.objects.create(
            organismo=self.organismo,
            referencia_pda="2.3",
            tipo_medida="Correctiva",
            nombre_corto="Reducción NOx",
            indicador=self.indicador,
            frecuencia="mensual",
            regulatoria="Sí"
        )

    def test_creacion_medida(self):
        """
        Verifica que la Medida se crea correctamente y su __str__ funciona.
        """
        self.assertEqual(str(self.medida), "Reducción NOx")


class ReporteModelTest(TestCase):
    """
    Pruebas unitarias para el modelo Reporte.
    """

    def setUp(self):
        """
        Crea los objetos necesarios: Organismo, Indicador, Medida y Reporte.
        """
        self.organismo = Organismo.objects.create(
            nombre="MINSAL", region="Biobío")
        self.indicador = Indicador.objects.create(
            descripcion="Índice de cumplimiento",
            formula_calculo="valor esperado / valor real",
            medio_verificacion="Sistema de monitoreo"
        )
        self.medida = Medida.objects.create(
            organismo=self.organismo,
            nombre_corto="Revisión de estándares",
            indicador=self.indicador
        )
        self.reporte = Reporte.objects.create(
            fecha="2024-01-01",
            año_calendario=2024,
            estado="pendiente",
            organismo=self.organismo,
            medida=self.medida
        )

    def test_creacion_reporte(self):
        """
        Verifica que un Reporte se crea correctamente y se representa como string.
        """
        self.assertEqual(str(self.reporte),
                         f"Reporte {self.reporte.id} - 2024-01-01")


class CumplimientoModelTest(TestCase):
    """
    Pruebas unitarias para el modelo Cumplimiento.
    """

    def setUp(self):
        """
        Crea una Medida para asociar al cumplimiento.
        """
        self.organismo = Organismo.objects.create(
            nombre="SEREMI", region="Araucanía")
        self.indicador = Indicador.objects.create(
            descripcion="Índice global",
            formula_calculo="A/B",
            medio_verificacion="Auditoría externa"
        )
        self.medida = Medida.objects.create(
            organismo=self.organismo,
            nombre_corto="Inspecciones",
            indicador=self.indicador
        )
        self.cumplimiento = Cumplimiento.objects.create(
            medida=self.medida,
            porcentaje_cumplimiento=82.5
        )

    def test_cumplimiento_str(self):
        """
        Verifica el __str__ del modelo Cumplimiento.
        """
        self.assertIn("82.5", str(self.cumplimiento))
