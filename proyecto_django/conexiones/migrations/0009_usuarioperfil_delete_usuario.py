# Generated by Django 5.1.5 on 2025-04-07 18:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conexiones', '0008_alter_cumplimiento_creado_por_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UsuarioPerfil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rol', models.CharField(choices=[('administrador', 'Administrador'), ('coordinador', 'Coordinador'), ('analista', 'Analista'), ('externo', 'Externo')], max_length=20)),
                ('organismo_asociado', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='conexiones.organismo')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'usuario_perfil',
            },
        ),
        migrations.DeleteModel(
            name='Usuario',
        ),
    ]
