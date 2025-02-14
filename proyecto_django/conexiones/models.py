from django.db import models



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


# DB Medidas
class Medida(models.Model):
    '''
    Representación de las medidas implementadas.
    Campos:
        'id_medida': Identificador único de la medida.
        'id_organismo': Referencia al id del organismo.
        'referencia_pda': Menciona apartado del pda.
        'tipo_medida': Si el campo 'regulatoria' es no regulatoria describe el tipo de medida.
        'nombre_corto': Nombre corto del indicador.
        'indicador': Descripción del indicador.
        'formula': Describe la fórmula del indicador.
        'frecuencia': Menciona cada cuanto se debe reportar el indicador.
        'verificacion': Medio verificador que especifica de que forma se debe entregar la medida.
        'regulatoria': Regulatoria o no regulatoria.
    '''
    id_medida = models.AutoField(primary_key=True)
    id_organismo = models.IntegerField() #Bryan: Podría hacer referencia al id_organismo
    referencia_pda = models.CharField(max_length=255, blank=True, null=True) #Bryan: debería ser ppda
    tipo_medida = models.CharField(max_length=255, blank=True, null=True)
    nombre_corto = models.CharField(max_length=None, blank=True, null=True)
    indicador = models.CharField(max_length=None, blank=True, null=True)
    formula = models.CharField(max_length=None, blank=True, null=True)
    frecuencia = models.CharField(max_length=255, blank=True, null=True)
    verificacion = models.CharField(max_length=None, blank=True, null=True)
    regulatoria = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'medidas'


class Reporte(models.Model):
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
    estado = models.CharField(max_length=50) #Crear categorías, quizás en el front
    id_organismo = models.ForeignKey(Organismo, on_delete=models.CASCADE)
    id_medida = models.ForeignKey(Medida, on_delete=models.CASCADE)
    #Falta el medio verificador

    def __str__(self):
        return f"Reporte {self.id_reporte} - {self.fecha}"


class Cumplimiento(models.Model):
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

class Usuario(models.Model):
    '''
    Tabla que crea la organización de usuarios.
    Campos:
        'id_usuario': Identificador único del usuario.
        'nombre': Nombre de usuario.
        'rol': Rol jerárquico del usuario.
        'organismo_asociado': A que organismo está asociado.
    '''
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    rol = models.CharField(max_length=100)
    organismo_asociado = models.ForeignKey(
        Organismo, on_delete=models.SET_NULL, null=True)

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
