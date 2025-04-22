# 📋 CHANGELOG

Todas las modificaciones importantes a este proyecto serán documentadas en este archivo.

---

## [Tercera Entrega] - 2025-05-24
### Agregado
- Se crea endpoint para la visualización de archivos `README.md` y `CHANGELOG.md` en la API.
- Se crea template HTML (`bienvenida.html`) para vista de `BienvenidaRootView`.
- Se crea registro de logs, para guardar información de las peticiones realizadas a la API.
- Se crea un endpoint para la visualización de logs en la API.
- Se crean variables de entorno para la configuración de la API.

### Cambiado
- Se modifica la vista `Bienvenida` para que devuelva un mensaje de bienvenida con los participantes del proyecto.
- Se eliminan los campos `id_medida`, `id_indicador`, `id_organismo`, `id_reporte` y `id_cumplimiento` de los modelos, ya que Django crea automáticamente un campo `id` autoincremental para cada modelo.
- Se cambia `serializers.py` para los nuevos modelos y se eliminan los campos innecesarios.

### Corregido
- Se añaden excepciones para manejar errores en la API.
  - Errores son guardados en el log de la API.
- Se agregaron validaciones de lógica de negocio al `MedidaSerializer` para asegurar coherencia entre los campos `regulatoria`, `frecuencia` y `tipo_medida`.
- Se incorporó logging en el serializer de `Medida` para registrar advertencias y errores durante la validación.



## [Segunda Entrega] - 2025-04-09
### Agregado
- Se agregan instrucciones de instalación en  `README.md` .
- Se agregan decoradores Swagger para la documentación de la API en `views.py`.
- Se añade CORS para permitir el acceso a la API desde otros dominios.
- Se añade autentificación tipo Basic Auth para la API.
  - Se agrega en `admin.py` clases para manipular los permisos de los usuarios en el admin de Django, vinculando los permisos de los usuarios a los grupos de Django.

### Cambiado
- Se actualizan descripciones de los modelos en `models.py`.
- Se modifica el usuario, se utiliza el usuario de Django en vez de un campo `usuario` en los modelos.
- Se genera modelo `UsuarioPerfil` para gestionar los perfiles de usuario, ligado a `User` de Django.


### Corregido (Oportunidades de Mejora)
- Se cambia a clave foráneas id_organismo en la tabla `Medida`
    - id_organismo = models.ForeignKey(Organismo, on_delete=models.CASCADE)
- `id_organismo` en `Medida` ahora es una clave foránea a `Organismo`.
  - organismo = models.ForeignKey(Organismo, on_delete=models.CASCADE)
- Se normalizó la relación entre `Medida` e `Indicador`: ahora `Medida` tiene una relación `ForeignKey` con `Indicador`.
- Eliminados campos redundantes en `Medida`: `formula`, `verificación`, y `indicador`.
- Se normalizaron los campos `frecuencia`, `estado` y `rol` utilizando `choices`, evitando valores inconsistentes y facilitando su gestión en formularios y admin.
- Se agregó una nueva entidad `PPDA` (Plan de Descontaminación) para representar el plan general de descontaminación de Concón-Quintero-Puchuncaví.
- Se añadió la entidad `PeriodoPPDA` para definir los distintos periodos (años, trimestres, etc.) dentro de un PPDA.
- Se estableció la relación entre `Medida` y `PPDA`, permitiendo asociar medidas específicas a un plan y su periodo correspondiente.


### Corregido (Mejoras Sugeridas)

#### Refactorizado
- Se refactorizó el modelo de datos para representar explícitamente el PPDA como entidad independiente.
- Se eliminó la redundancia entre `Medida` e `Indicador`; ahora `Medida` contiene una clave foránea a `Indicador`.
- Se agregó el modelo `PeriodoPPDA` para representar fases anuales o temporales dentro del PPDA.
- Se actualizaron las relaciones entre `Medida`, `PPDA` y `PeriodoPPDA` para mayor claridad y normalización del esquema.

#### Uso de choices
- Se aplicaron `choices` en los campos `estado`, `frecuencia`, `rol` y `regulatoria` para limitar valores válidos y mejorar la consistencia del modelo.

#### Uso de TimeStamps
- Se incorporaron campos de trazabilidad (`created_at`, `updated_at`, `creado_por`, `modificado_por`) mediante una clase base abstracta `Trazable`.
- Los modelos `Medida`, `Reporte` y `Cumplimiento` heredan ahora de `Trazable`, permitiendo registrar automáticamente el historial de creación y modificación de cada registro.

#### Tabla Intermedia para asignaciones
- Se incorporó el modelo `AsignacionIndicador`, que permite registrar la asignación de indicadores a organismos por parte de SMA, incluyendo campos como fecha de asignación y observaciones.