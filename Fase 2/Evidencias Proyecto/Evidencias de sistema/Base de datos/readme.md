1. Requisitos del Sistema
Para un correcto funcionamiento de la base de datos y la integración con el proyecto Django, se requieren las siguientes instalaciones:
´´´
MySQL Server$\ge 8.4.0$mysql-8.4.7-winx64.msiMySQL Workbench$\ge 8.0.0$mysql-workbench-community-8.0.44-winx64.msi
´´´
2. Instalación de MySQL Server y Workbench (Windows)
Instalar MySQL Server:

Ejecuta el instalador mysql-8.4.7-winx64.msi.

Selecciona la opción de instalación de Servidor solamente (o Custom para elegir solo el Server).

Durante la configuración, se te pedirá crear una contraseña para el usuario root. Guarda esta contraseña, ya que la necesitarás para el archivo .env.

Instalar MySQL Workbench:

Ejecuta el instalador mysql-workbench-community-8.0.44-winx64.msi. Esta herramienta es opcional pero altamente recomendada para la gestión gráfica de la base de datos.

3. Configuración del Proyecto Python/Django
3.1. Instalación de Dependencias
Para que Django pueda conectarse con MySQL, es necesario instalar el adaptador mysqlclient.

Asegúrate de estar en tu entorno virtual de Python ((venv) activado).

Instala todas las dependencias del proyecto:

´´´
(venv)  pip install -r requirements.txt
´´´
3.2. Configuración del Archivo .env
El proyecto utiliza un archivo .env para almacenar credenciales sensibles.

Localiza o crea el archivo .env en la raíz del proyecto.

Verifica y ajusta los siguientes parámetros con tus credenciales.

Si utilizaste una contraseña distinta a root durante la instalación del servidor, debes cambiar la variable DB_PASSWORD a la contraseña que definiste.
´´´
DB_PASSWORD=**** # <--- ¡CAMBIA ESTO!
´´´
4. Inicialización y Carga de Datos
Una vez configurado el servidor y el proyecto, procede a la carga del esquema y los datos.

4.1. Creación del Esquema de la Base de Datos
El archivo SIPstoreDB.sql contiene la exportación completa de la estructura de la base de datos (CREATE TABLE, etc.).

Ejecuta el siguiente comando en la terminal, asegurándote de usar la ruta correcta a tu archivo SQL:

´´´

(venv) $ mysql -u root -p < "C:\Users\...\SIPstoreDB.sql"
´´´
(Ingresa la contraseña del usuario root cuando se solicite).

4.2. Carga de Datos de Prueba
El archivo insert_pruebas.sql contiene todos los INSERT necesarios para poblar las tablas con datos de prueba (40 Paneles, 40 Kits, 40 Pedidos, etc.).

Ejecuta el siguiente comando, especificando la base de datos sipstoredb (la cual fue creada en el paso anterior):

´´´
(venv) $ mysql -u root -p sipstoredb < "C:\Users\...\insert_pruebas.sql"
´´´
