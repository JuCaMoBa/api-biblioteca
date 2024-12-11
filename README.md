# Aplicación FastAPI con Docker y PostgreSQL

Esta aplicación utiliza FastAPI como backend, Docker y PostgreSQL como base de datos. Sigue los pasos a continuación para configurar y ejecutar la aplicación.

## **Requisitos previos**

Antes de comenzar, asegúrate de tener instalados los siguientes programas en tu máquina:

- [Python 3.8 o superior](https://www.python.org/)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## **Pasos para la configuración**

1. **Renombrar el archivo `.env.example`**
   - En la raíz del proyecto encontrarás un archivo llamado `.env.example`.
   - Renómbralo como `.env`:

   - Dentro de `.env`, configura los valores para las siguientes variables:
     - `DB_USER`: Usuario de la base de datos.
     - `DB_PASSWORD`: Contraseña de la base de datos.
     - `DB_DATABASE`: Nombre de la base de datos.
     - `DB_HOST`: renombrar con el nombre de la carpeta principal donde esta el código puede ser nombre_de_carpeta-db-1

   - Por defecto, puedes usar:
     ```     
     DB_USER=postgres
     DB_PASSWORD=postgres
     DB_DATABASE=postgres
     DB_HOST=api-biblioteca-db-1
     ```

    las demás variables déjalas como están. 

2. **Crear un entorno virtual**
   - Crea un entorno virtual en la carpeta root del proyecto:
     ```
     python3 -m venv .venv
     ```
   - Activa el entorno virtual:
     - En **Linux/macOS**:
       ```
       source .venv/bin/activate
       ```
     - En **Windows**:
       ```
       .venv\Scripts\activate
       ```

3. **Instalar las dependencias**
   - Con el entorno virtual activado, instala las dependencias necesarias desde el archivo `requirements.txt`:
     ```
     pip install -r requirements.txt
     ```

4. **Construir y ejecutar los contenedores**
   - Construye y ejecuta los contenedores con Docker Compose:
     ```
     docker-compose up -d
     ```
   - Verifica que los contenedores estén en funcionamiento:
     ```
     docker ps
     ```
     Deberías ver al menos dos servicios en ejecución: `web` (FastAPI) y `db` (PostgreSQL).

5. **Comprobación de la API**
   - Una vez que los contenedores estén en ejecución, puedes acceder a la API de FastAPI en la siguiente URL:
     ```
     http://localhost:5000
     ```
   - La documentación interactiva(Swagger) de la API estará disponible en:
     ```
     http://localhost:5000/docs
     ```

¡Listo! Ya puedes usar y probar la aplicación. 🎉
