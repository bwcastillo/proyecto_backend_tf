# Generated by Django 5.1.5 on 2025-04-07 15:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conexiones', '0006_cumplimiento_creado_por_cumplimiento_created_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AsignacionIndicador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_asignacion', models.DateField()),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('activo', models.BooleanField(default=True)),
                ('indicador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conexiones.indicador')),
                ('organismo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conexiones.organismo')),
            ],
            options={
                'db_table': 'asignaciones_indicador',
                'unique_together': {('organismo', 'indicador')},
            },
        ),
    ]
