from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Opciones para frecuencia de reporte
FRECUENCIA_CHOICES = [
    ('diaria', 'Diaria'),
    ('semanal', 'Semanal'),
    ('mensual', 'Mensual'),
    ('trimestral', 'Trimestral'),
    ('anual', 'Anual'),
]

# Opciones de estado para el modelo Reporte
ESTADO_CHOICES = [
    ('pendiente', 'Pendiente'),
    ('enviado', 'Enviado'),
    ('rechazado', 'Rechazado'),
    ('aceptado', 'Aceptado'),
]

# Opciones de rol para el modelo Usuario
ROL_CHOICES = [
    ('administrador', 'Administrador'),
    ('coordinador', 'Coordinador'),
    ('analista', 'Analista'),
    ('externo', 'Externo'),
]


class Trazable(models.Model):
    """
    Modelo abstracto que añade campos de trazabilidad y timestamps.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creado_por = models.ForeignKey(User, related_name='%(class)s_creado_por', on_delete=models.SET_NULL, null=True, blank=True)
    modificado_por = models.ForeignKey(User, related_name='%(class)s_modificado_por', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        abstract = True


class PPDA(models.Model):
    """
    Representa el Plan de Descontaminación (PPDA) de Concón-Quintero-Puchuncaví.
    Campos:
        'nombre': Nombre del PPDA.
        'fecha_inicio': Fecha de inicio del PPDA.
        'fecha_fin': Fecha de fin del PPDA.
    """
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'ppda'


class PeriodoPPDA(models.Model):
    """
    Representa un periodo (año o fase) dentro del PPDA.
    Campos:
        'ppda': Relación con el PPDA al que pertenece este periodo.
        'anio': Año o periodo específico.
        'inicio_periodo': Fecha de inicio del periodo.
        'fin_periodo': Fecha de fin del periodo.
    """
    ppda = models.ForeignKey(PPDA, on_delete=models.CASCADE)
    anio = models.IntegerField()
    inicio_periodo = models.DateField()
    fin_periodo = models.DateField()

    def __str__(self):
        return f"Periodo {self.anio} del PPDA {self.ppda.nombre}"

    class Meta:
        db_table = 'periodos_ppda'


# DB Organismos
class Organismo(models.Model):
    '''
    Modelo de los Organismos presentes en el PPDA de Concón-Quintero-Puchuncaví.
    Campos:
        'id_organismo': id del organismo.
        'nombre': nombre del organismo.
        'region': región a la que emplaza.
    '''
    id_organismo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    region = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'organismos'
    
    def __str__(self):
        return self.nombre


class Indicador(models.Model):
    '''
    Tabla que detalla el desarrollo del indicador.
    Campos:
        'id_indicador':Identificador único del indicador.
        'descripcion': Describe de que trata el indicador.
        'formula_calculo': Describe la fórmula de cálculo del indicador.
        'medio_verificacion': Detalla el medio de verificación asociado.
    '''
    id_indicador = models.AutoField(primary_key=True)
    descripcion = models.TextField()
    formula_calculo = models.TextField()
    medio_verificacion = models.TextField() #Debería agregarse a un posible campo de medio de verificación 

    def __str__(self):
        return self.descripcion


# DB Medidas
class Medida(Trazable):
    '''
    Representación de las medidas implementadas.
    Campos:
        'id_medida': Identificador único de la medida.
        'id_organismo': Referencia al id del organismo.
        'referencia_pda': Menciona apartado del pda.
        'tipo_medida': Si el campo 'regulatoria' es no regulatoria describe el tipo de medida.
        'nombre_corto': Nombre corto del indicador.
        'frecuencia': Menciona cada cuanto se debe reportar el indicador.
        'regulatoria': Regulatoria o no regulatoria.
    '''
    id_medida = models.AutoField(primary_key=True)
    organismo = models.ForeignKey(Organismo, on_delete=models.CASCADE)
    referencia_pda = models.CharField(max_length=255, blank=True, null=True)
    tipo_medida = models.CharField(max_length=255, blank=True, null=True)
    nombre_corto = models.CharField(max_length=255, blank=True, null=True)

    # Nueva relación
    indicador = models.ForeignKey('Indicador', on_delete=models.SET_NULL, null=True)

    frecuencia = models.CharField(
        max_length=20,
        choices=FRECUENCIA_CHOICES,
        blank=True,
        null=True
    )
    regulatoria = models.CharField(max_length=255, blank=True, null=True)
    
    # Vinculacion con PPDA y PeriodoPPDA
    ppda = models.ForeignKey('PPDA', on_delete=models.CASCADE, null=True, blank=True)
    periodo_ppda = models.ForeignKey('PeriodoPPDA', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'medidas'
    
    def __str__(self):
        return self.nombre_corto or f"Medida {self.id_medida}"


class Reporte(Trazable):
    '''
    Modelo de datos que recepciona los reportes de los entidad con responsabilidad ambiental.
    Campos:
        'id_reporte': Identificador único del reporte.
        'fecha': Fecha de entrega del reporte.
        'año_calendario': Espeicifica el año del calendario.
        'estado': En que estado está el reporte.
        'id_organismo': Identificador único del organismo asociado.
        'id_medida': Que medida agrega.
    '''
    id_reporte = models.AutoField(primary_key=True)
    fecha = models.DateField()
    año_calendario = models.IntegerField() #Normalizar para entregar opciones, quizás en el Front
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES
    )
    id_organismo = models.ForeignKey(Organismo, on_delete=models.CASCADE)
    id_medida = models.ForeignKey(Medida, on_delete=models.CASCADE)
    #Falta el medio verificador

    def __str__(self):
        return f"Reporte {self.id_reporte} - {self.fecha}"


class Cumplimiento(Trazable):
    '''
    Tabla que detalla el avance y porcentaje de cumplimiento por indicador.
    Campos:
        'id_cumplimiento': Identificador único.
        'id_medida': Identificador único de las medidas asociadas.
        'porcentaje_cumplimiento': En que porcentaje está cumplida esta medida.
    '''
    id_cumplimiento = models.AutoField(primary_key=True)
    id_medida = models.ForeignKey(Medida, on_delete=models.CASCADE)
    porcentaje_cumplimiento = models.DecimalField(
        max_digits=5, decimal_places=2)
    #Considerar agregar medio de verificación

    def __str__(self):
        return f"{self.id_medida} - {self.porcentaje_cumplimiento}%"


class AsignacionIndicador(models.Model):
    """
    Representa la asignación de un indicador desde la SMA a un organismo específico.
    """
    organismo = models.ForeignKey(Organismo, on_delete=models.CASCADE)
    indicador = models.ForeignKey(Indicador, on_delete=models.CASCADE)
    fecha_asignacion = models.DateField()
    observaciones = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.indicador.descripcion} → {self.organismo.nombre}"

    class Meta:
        db_table = 'asignaciones_indicador'
        unique_together = ('organismo', 'indicador')


class UsuarioPerfil(models.Model):
    '''
    Extiende el modelo de usuario de Django para asociar un rol y un organismo.
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=ROL_CHOICES)
    organismo_asociado = models.ForeignKey(Organismo, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.rol})"

    class Meta:
        db_table = 'usuario_perfil'


@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        UsuarioPerfil.objects.create(
            user=instance,
            rol='externo'  # rol por defecto
        )


@receiver(post_save, sender=User)
def guardar_perfil_usuario(sender, instance, **kwargs):
    instance.usuarioperfil.save()