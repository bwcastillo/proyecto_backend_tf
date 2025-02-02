# Generated by Django 5.1.5 on 2025-01-28 21:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Indicador',
            fields=[
                ('id_indicador', models.AutoField(primary_key=True, serialize=False)),
                ('descripcion', models.TextField()),
                ('formula_calculo', models.TextField()),
                ('medio_verificacion', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Medida',
            fields=[
                ('id_medida', models.AutoField(primary_key=True, serialize=False)),
                ('descripcion', models.TextField()),
                ('tipo', models.CharField(max_length=100)),
                ('plazo', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Organismo',
            fields=[
                ('id_organismo', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('tipo', models.CharField(max_length=100)),
                ('region', models.CharField(max_length=100)),
                ('contacto', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Cumplimiento',
            fields=[
                ('id_cumplimiento', models.AutoField(primary_key=True, serialize=False)),
                ('porcentaje_cumplimiento', models.DecimalField(decimal_places=2, max_digits=5)),
                ('id_medida', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conexiones.medida')),
            ],
        ),
        migrations.AddField(
            model_name='medida',
            name='id_organismo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conexiones.organismo'),
        ),
        migrations.CreateModel(
            name='Reporte',
            fields=[
                ('id_reporte', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField()),
                ('año_calendario', models.IntegerField()),
                ('estado', models.CharField(max_length=50)),
                ('id_medida', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conexiones.medida')),
                ('id_organismo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conexiones.organismo')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id_usuario', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('rol', models.CharField(max_length=100)),
                ('organismo_asociado', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='conexiones.organismo')),
            ],
        ),
    ]
