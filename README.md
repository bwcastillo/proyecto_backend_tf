# Feedback: curso Backend en Python de Talento Futuro, Corfo.

Este es un repositorio que contiene el proyecto del curso Backend en Python de Talento Futuro, Corfo. 

## **I. Sprint 1 - Semana 1 (30 de enero al 15 de febrero):**
**Tareas del equipo**:
|Tarea|Responsable(s)|Fecha entrega|Finalizado|
|-----|--------|-------------|---|
|Avance HU (en Taiga y otra herramienta similar) | Bryan |01FEB|<ul><li> [X] Finalizado</li><ul> |
|Avance de normalizacion de datos | Scarlett| 31ENER - 01FEB| <ul><li> [X] Finalizado</li><ul> |
|Avance de código Core 1(Django| Manuel | 31ENE - 02FEB - 03FEB| <ul><li> [X] Finalizado</li><ul>|
|Avance de código Core 2(Django)| Ulises | 31ENE - 02FEB - 03FEB| <ul><li> [X] Finalizado</li><ul>|
|Testing Carol - Bryan | Carol (Tester)| 31ENE - 02FEB - 03FEB| <ul><li> [X] Finalizado</li><ul>|
|Documentación de APIs (Swagger)| Manuel - Ulises | 02FEB | <ul><li> [X] Finalizado</li><ul> |
|Demo funcional en video (link a YouTube, oculto)| Ulises - Bryan| 03FEB-04FEB-05FEB|<ul><li> [X] Finalizado</li><ul>|

- [X] LUNES 03 FEBRERO: AMISTOSOS RECORDATORIOS 
- [X] LUNES 10 FEBRERO: REVISIÓN - ENTREGABLES 
- [X] LUNES 10 FEBRERO: EMPAQUETAMIENTO - VIDEO - COORDINA LA ENTREGA EL COMO 

La revisión y reporte de este Sprint estarán disponibles en el siguiente [link](/administrativo/revisiones)


## **II. Lógica del negocio y Backlogs**

```mermaid
sequenceDiagram
    participant PPDA
    participant Fiscalizador
    participant Organismo responsable
    PPDA->> Fiscalizador: BL0: Recibe PPDA con indicaciones
    Fiscalizador->>Organismo responsable: BL1: Manda indicadores 
    Organismo responsable->>Fiscalizador: BL2: Cumple con los índices y manda reporte
    Fiscalizador->>Organismo responsable: BL 0.1: Verifica cumplimiento y notifica cumplimiento
```


<br>

## **III. Backlog:** 


**Parte 0**
- Llega resolucion
- Cada artículo de la resolución es un organismo con una tabla de responsabilidades.
- El fiscalizador tiene que mandar las tablas a cada organismo responsable

**Tareas Core 1 (Fiscalizador | Encargado: Manuel D.):**
- Poder introducir/elegir organismos
- Escribirles las tareas(indicadores) a los organismos responsable
- Mandar las tareas y los respectivos indicadores a los organismos responsables

**Tareas Core 2 (Entidad responsable | Encargado: Ulises C.:**
- COMO CLIENTE (ORGANISMO RESPONSABLE)
- IDEALMENTE QUIERO SER NOTIFICADO CON LAS MEDIDAS QUE TENGO COMO CUMPLIR
Y CON UN DEAD LINE (FRECUENCIA DEL REPORTE)

**Tareas parte 3 (por definir):**
- COMO CLIENTE UNA VEZ REALICE LAS MEDIDAS QUIERO POSTEARLAS AL FISCALIZADOR

**Lujo Bonus track):**
- Parte 0
- PEDIR PRORROGA
-	FISCALIZADOR APRUEBA TERMINADO
-	FISCALIZADOR APRUEBA DA PRORROGA (PREGUNTAR A STANLEY)
-	FISCALIZADOR DA CUENTA NO CUMPLE
    - SI NO CUMPLE MANDA RECORDATORIO O MULTA (REVISAR)

## Historia
1) Yo como fiscalizador tengo que mandar los indicadores por cumplir a los organismos sectoriales. (PREGUNTAR) Sin embargo, en la práctica el fiscalizador debería activar un método para que el organismo sectorial permita postear en la tabla los campos que se llenan. 
Nico creará un front dónde se usa este método para que el usuario pueda rellenar el formulario
2) Yo como organismo sectorial ya notificado o sabiendo que tengo que rellenar (POST) la tabla del formulario. 


--

## **IV. Instalación y uso**

Para instalar el proyecto, sigue estos pasos:

### 1. Clonar el repositorio

```bash
git clone hhttps://github.com/bwcastillo/proyecto_backend_tf
cd proyecto_backend_tf/proyecto_django/
```

### 2. Crear un entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # En Linux/Mac
# o
venv\Scripts\activate  # En Windows
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar la base de datos
- Asegúrate de tener PostgreSQL instalado y en funcionamiento.
- Crea una base de datos para el proyecto.
- Configura la conexión a la base de datos en el archivo `settings.py` de Django.

### 5. Ejecutar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6 De ser necesario, crear un superusuario para acceder al panel de administración de Django:

```bash
python manage.py createsuperuser
```

### 7. Ejecutar el servidor de desarrollo

```bash
python manage.py runserver
```

