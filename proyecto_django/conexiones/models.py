from django.db import models


# DB Organismos
class Organismo(models.Model):
    id_organismo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    region = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'organismos'


# DB Medidas
class Medida(models.Model):
    id_medida = models.AutoField(primary_key=True)
    id_organismo = models.IntegerField()
    referencia_pda = models.CharField(max_length=255, blank=True, null=True)
    tipo_medida = models.CharField(max_length=255, blank=True, null=True)
    nombre_corto = models.CharField(max_length=255, blank=True, null=True)
    indicador = models.CharField(max_length=255, blank=True, null=True)
    formula = models.CharField(max_length=255, blank=True, null=True)
    frecuencia = models.CharField(max_length=255, blank=True, null=True)
    verificacion = models.CharField(max_length=255, blank=True, null=True)
    regulatoria = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'medidas'


class Reporte(models.Model):
    id_reporte = models.AutoField(primary_key=True)
    fecha = models.DateField()
    año_calendario = models.IntegerField()
    estado = models.CharField(max_length=50)
    id_organismo = models.ForeignKey(Organismo, on_delete=models.CASCADE)
    id_medida = models.ForeignKey(Medida, on_delete=models.CASCADE)

    def __str__(self):
        return f"Reporte {self.id_reporte} - {self.fecha}"


class Cumplimiento(models.Model):
    id_cumplimiento = models.AutoField(primary_key=True)
    id_medida = models.ForeignKey(Medida, on_delete=models.CASCADE)
    porcentaje_cumplimiento = models.DecimalField(
        max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.id_medida} - {self.porcentaje_cumplimiento}%"


class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    rol = models.CharField(max_length=100)
    organismo_asociado = models.ForeignKey(
        Organismo, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nombre


class Indicador(models.Model):
    id_indicador = models.AutoField(primary_key=True)
    descripcion = models.TextField()
    formula_calculo = models.TextField()
    medio_verificacion = models.TextField()

    def __str__(self):
        return self.descripcion
