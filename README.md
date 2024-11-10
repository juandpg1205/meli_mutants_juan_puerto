# Meli_mutants_juan_puerto
Este es el repositorio creado para alojar el desafio para aplicar a meli como ingeniero de datos


# Mutant Detection API

## Resumen del Proyecto

Este proyecto consiste en la creación de una API que permite identificar si una secuencia de ADN pertenece a un mutante o no. La API está desarrollada en Python utilizando **Flask** y **SQLAlchemy** y se despliega en **Google Cloud Run** conectándose a una base de datos **Cloud SQL** especificamente en **PostgreSQL** para almacenar las secuencias de ADN. La base de datos evita la duplicidad de registros y permite realizar consultas de las secuencias analizadas.

## Uso Funcional

### Endpoints de la API


1. **LEVEL2: POST /mutant**
   - **URL**: https://mutant-api-368177300157.northamerica-northeast1.run.app/mutant
   - **Descripción**: Determina si la secuencia de ADN corresponde a un mutante.
   - **Ejemplo de Solicitud**:
     ```json
     {
       "dna": ["ATGCGA", "CAGTGC", "TTATGT", "AGAAGG", "CCCCTA", "TCACTG"]
     }
     ```
   - **Respuesta**:
     - `200 OK`: Mutant detected.
     - `403 Forbidden`: Not a mutant.

2. **LEVEL 3: GET /stats**
   - **URL**: https://mutant-api-368177300157.northamerica-northeast1.run.app/stats
   - **Descripción**: Devuelve estadísticas sobre las secuencias almacenadas.
   - **Ejemplo de Respuesta**:
     ```json
     {
       "count_mutant_dna": 40,
       "count_human_dna": 100,
       "ratio": 0.4
     }
     ```

### Componentes Técnicos

1. **Algoritmo de Detección de Mutantes**:
   - El algoritmo analiza la matriz de ADN buscando secuencias de 4 letras idénticas en sentido horizontal, vertical o diagonal.
   - Si encuentra más de una secuencia de este tipo, determina que el ADN corresponde a un mutante.

2. **Base de Datos**:
   - Se usa **SQLAlchemy** como ORM para gestionar la base de datos.
   - El modelo `DNASequence` se creó para almacenar cada secuencia de ADN y si pertenece a un mutante o no.
   - Antes de almacenar una nueva secuencia, el programa verifica si ya existe para evitar la duplicación de registros.

3. **Cloud SQL y Cloud Run**:
   - La API fue diseñada para ser desplegada en **Google Cloud Run** y conectarse a una instancia de **Cloud SQL**.
   - Se configuraron variables de entorno y un conector para gestionar la conexión a la base de datos de manera segura.

4. **API REST**:
   - La API cuenta con un endpoint `/mutant` que recibe una secuencia de ADN en formato JSON y responde si la secuencia corresponde a un mutante.
   - El endpoint `/stats` devuelve estadísticas sobre cuántas secuencias corresponden a mutantes y cuántas a humanos.

### Estructura del Código
- `mutant_detector.py`: Contiene el algoritmo de detección de ADN mutante.
- `mutant_api.py`: Define los endpoints de la API y la conexión con la base de datos.
- `requirements.txt`: Archivo de dependencias para instalar los paquetes necesarios.

## Instrucciones para Replicar el Programa o API

### Requisitos Previos
- **Python 3.9+** instalado.
- **Docker** instalado para ejecutar el contenedor localmente.
- **Google Cloud SDK** si deseas desplegar la API en **Google Cloud Run**.
- **Cloud SQL Auth Proxy** si deseas probar localmente con una base de datos en Cloud SQL.

## Notas Finales
- La base de datos guarda cada secuencia de ADN única para evitar el almacenamiento redundante.
- Antes de desplegar, es necesario configurar correctamente los permisos de la cuenta de servicio en **Cloud SQL** para permitir la conexión segura desde **Cloud Run**.

Si tienes alguna duda o necesitas más información contáctame.

