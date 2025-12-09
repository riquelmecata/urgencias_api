# Sistema de Gestión de Urgencias 🏥

Plataforma web integral para la gestión del flujo de pacientes en servicios de urgencia hospitalaria. El sistema digitaliza el proceso desde el ingreso pre-hospitalario por paramédicos, pasando por el triaje de enfermería, hasta el diagnóstico y alta médica.

## 🚀 Tecnologías Utilizadas

### Backend & Integración
* **Lenguaje:** Python 3.10
* **Framework:** Django & Django REST Framework (DRF)
* **Base de Datos:** SQLite (Local) / MySQL (Producción)
* **Arquitectura:** Monolítica (Frontend integrado en Backend mediante `frontend_build`).

### Frontend
* **Librería:** React.js (Pre-compilado para producción).
* **Estilos:** Bootstrap 5 & CSS personalizado.
* **Consumo API:** Fetch API.

### Infraestructura
* **Despliegue:** PythonAnywhere.
* **Archivos:** Gestión de estáticos (Whitenoise/Collectstatic) y media.

---

## 📋 Funcionalidades por Perfil

### 🚑 1. Perfil Paramédico
* Formulario de ingreso rápido de pacientes.
* Registro de signos vitales.
* **Carga de Evidencia:** Subida de fotografías del accidente.

### 👩‍⚕️ 2. Perfil Enfermera
* Visualización de pacientes en espera.
* **Triaje:** Asignación de prioridad (Alta/Media/Baja).
* Derivación a médico.

### 👨‍⚕️ 3. Perfil Doctor
* Recepción de casos derivados.
* Visualización de ficha clínica y evidencias.
* Registro de Diagnóstico y Alta.

### 🛡️ 4. Perfil Administrador (Jefe)
* **Dashboard de Auditoría:** Historial completo de acciones (Log de eventos).
* Gestión de usuarios y accesos.

---

## ⚙️ Instalación y Ejecución Local

Este proyecto utiliza una arquitectura unificada. **No se requiere Node.js ni NPM para ejecutar la aplicación**, ya que el frontend se encuentra compilado e integrado dentro de Django.

### Pasos para ejecutar:

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/TU_USUARIO/urgencias_api.git](https://github.com/TU_USUARIO/urgencias_api.git)
    cd urgencias_api
    ```

2.  **Configurar Entorno Virtual e Instalar Dependencias:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # (En Windows: venv\Scripts\activate)
    pip install -r requirements.txt
    ```

3.  **Preparar Base de Datos:**
    ```bash
    python manage.py migrate
    python manage.py createsuperuser  # (Opcional: Para crear un admin)
    ```

4.  **Correr el Servidor:**
    ```bash
    python manage.py runserver
    ```

5.  **¡Listo!**
    Abre tu navegador en `http://127.0.0.1:8000/`.
    *Django servirá automáticamente la aplicación React y la API.*

