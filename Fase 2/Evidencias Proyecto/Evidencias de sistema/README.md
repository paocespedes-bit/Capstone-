
----------
#  Manual de Instalación — Sistema SIPstore

Este documento describe el proceso de instalación, configuración y despliegue del sistema **SIPstore**, incluyendo requisitos, dependencias, preparación del entorno, inicialización de la base de datos y ejecución del proyecto.

----------

##  1. Introducción

### **1.1 Propósito**

Proporcionar las instrucciones necesarias para instalar, configurar y ejecutar el sistema **SIPstore** en sus diferentes ambientes de desarrollo y pruebas.

### **1.2 Alcance**

Este manual cubre:

-   Instalación del entorno de Python.
    
-   Configuración del proyecto Django.
    
-   Preparación de la base de datos MySQL.
    
-   Ejecución del servidor.
    
-   Configuración de servicios externos (SendGrid, Mercado Pago).
    
-   Manejo de archivos estáticos.
    

**Ambientes abordados:**

-   **Desarrollo (local)**
    
-   **Pruebas (QA)**
    

----------

##  2. Requisitos Previos

### **2.1 Hardware**
|Componente  |Mínimo  | Recomendado |
|--|--|--|
| CPU | Dual-Core 2.0 GHz | Quad-Core|
|RAM|4 GB|8 GB o más|
|Almacenamiento|10 GB libres|20 GB en SSD|
|Internet|Acceso estable|Banda ancha (≥5 Mbps)|

----------

### **2.2 Software Requerido**

|Categoría|Requisito|Versión|
|--|--|--|
|Sistema Operativo|Windows / Linux|Últimas versiones|
|Python|Python|**3.13.7**|
|Entornos|venv|Última versión|
|Navegador|Chrome / Firefox / Edge|Última versión|
|Gestor de Paquetes|pip|Última versión|

----------

### **2.3 Dependencias del Sistema**

-   **Base de datos:** MySQL **8.4.7**
    
-   **Cliente recomendado:** MySQL Workbench **8.0.44**
    
-   **Servicios externos:**
    
    -   SendGrid (API Key)
        
    -   Mercado Pago Checkout Pro (Client ID / Secret)
        

----------

##  3. Instalación

### **3.1 Descarga del Proyecto**

Clonar el repositorio:

```
git clone https://github.com/paocespedes-bit/Capstone-.git
```

Ingresar al directorio del proyecto:

```
cd "Capstone-/Fase 2/Evidencias Proyecto/Evidencias de sistema/Aplicación/SIPstore/"
```

----------

### **3.2 Instalación de Dependencias**

Crear entorno virtual:

```
pip install virtualenv
python -m venv venv
```

Activación:

**Windows:**

```
venv\Scripts\activate
```

**Linux/macOS:**

```
source venv/bin/activate
```

Instalar librerías:

```
(venv) pip install -r requirements.txt
```

----------

### **3.3 Configuración del Archivo `.env`**

Crear un archivo `.env` en el directorio raíz e incluir:

```
SECRET_KEY=django-insecure-h8pccql3...
DEBUG=True
DB_PASSWORD=root
MERCADOPAGO_PUBLIC_KEY=SU_CLAVE
MERCADOPAGO_ACCESS_TOKEN=SU_TOKEN
SENDGRID_API_KEY=SU_API_KEY
EMAIL_HOST_PASSWORD=SU_API_KEY
```

 **Sin comillas y sin espacios.**

----------

### **3.4 Inicialización del Sistema**

#### **1. Crear la base de datos**

```
mysql -u root -p
CREATE DATABASE SIPstoreDB;
EXIT;
```

#### **2. Migraciones**

```
(venv) python manage.py makemigrations
(venv) python manage.py migrate
```

#### **3. Cargar datos de prueba (opcional)**

```
mysql -u root -p SIPstoreDB < "C:\ruta\insert_pruebas.sql"
```

#### **4. Crear superusuario**

```
(venv) python manage.py createsuperuser
```

**Usar correo:** `tonopanelessip@gmail.com`

----------

##  4. Ejecución del Sistema

### **4.1 Configurar Ngrok (para uso con APIs externas)**

Configurar token:
```
ngrok authtoken SU_TOKEN
```

----------

### **4.2 Ejecutar el servidor**

**Terminal 1 (Django)**

```
(venv) python manage.py runserver
```

**Terminal 2 (ngrok)**

```
ngrok http 8000
```

----------

### **4.3 Acceso al Sistema**

-   Acceso local:  
 `http://127.0.0.1:8000`
    
    
-   Acceso público mediante Ngrok (HTTPS):  
    `https://xxxx.ngrok-free.app`
    

----------

##  Sistema listo para uso en entornos de desarrollo y QA

