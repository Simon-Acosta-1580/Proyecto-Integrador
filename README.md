<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>README | Proyecto Impacto Mundial - SGA</title>
</head>
<body>

    <h1>Proyecto Impacto Mundial — Sistema de Gestión de Analíticas (SGA)</h1>

    <h2>Descripción General</h2>
    <p>Este proyecto implementa un Sistema de Gestión de Analíticas (SGA) diseñado para centralizar y estandarizar la creación y seguimiento de metodologías de análisis de datos. Su propósito es gestionar usuarios, definir metodologías de investigación y registrar análisis específicos (como impacto en medios o participación en redes).</p>
    <p>El proyecto se desarrolla utilizando una arquitectura basada en el <i>Model-View-Controller</i> (MVC) ligero, con Python en el backend y Jinja2 para la capa de presentación.</p>

    <hr>

    <h2>Tecnologías Utilizadas</h2>

    <h3>Backend y Estructura</h3>
    <ul>
        <li><strong>Python 3.11+</strong></li>
        <li><strong>FastAPI / Starlette</strong> — Framework principal para la lógica de negocio y enrutamiento.</li>
        <li><strong>Jinja2</strong> — Motor de plantillas para renderizar el HTML dinámico (la 'Vista').</li>
    </ul>

    <h3>Frontend</h3>
    <ul>
        <li><strong>HTML5, CSS3, JavaScript</strong></li>
        <li><strong>Bootstrap 5.3</strong> — Framework CSS para el diseño responsivo y la interfaz de usuario.</li>
        <li><strong>Jinja2 Templating</strong> — Utilizado para la herencia de plantillas (<code>{% extends 'header.html' %}</code>) que garantiza una estructura HTML válida y consistente.</li>
    </ul>

    <hr>

    <h2>Estructura del Proyecto</h2>
    <p>La aplicación sigue una estructura modular donde el código de las rutas y el manejo de plantillas están separados por módulos temáticos.</p>

    <pre style="background-color: #eee; padding: 10px; border: 1px solid #ccc; overflow-x: auto;">
Proyecto-Integrador/
├── main.py (Configuración de FastAPI y routers principales)
├── db/ (Manejo de la conexión a la base de datos)
├── routers/
│   ├── users.py (Rutas para gestión de Usuarios)
│   ├── metodologias.py (Rutas para gestión de Metodologías)
│   └── analisis.py (Rutas para gestión de Análisis)
└── templates/
    ├── header.html (Plantilla base con &lt;head&gt;, &lt;body&gt;, navbar y footer)
    ├── index.html (Página de inicio)
    ├── _navbar.html (Fragmento de navegación)
    ├── _footer.html (Fragmento de pie de página)
    └── ... otras vistas (ej. analisis_new.html, users_list.html)
</pre>

    <hr>

    <!-- Configuración del Entorno -->
    <h2>Configuración del Entorno</h2>
    <p>Sigue estos pasos para poner en marcha el proyecto en tu entorno local.</p>
    <ol>
        <li>Clonar el repositorio:<br>
            <pre style="background-color: #333; color: white; padding: 10px; overflow-x: auto;"><code>git clone https://github.com/Simon-Acosta-1580/Proyecto-Integrador.git</code></pre>
        </li>
        <li>Crear entorno virtual:<br>
            <pre style="background-color: #333; color: white; padding: 10px; overflow-x: auto;"><code>python -m venv .venv</code></pre>
        </li>
        <li>Activar entorno virtual:<br>
            <pre style="background-color: #333; color: white; padding: 10px; overflow-x: auto;"><code>.venv\Scripts\activate   # (Windows)</code></pre>
            <pre style="background-color: #333; color: white; padding: 10px; overflow-x: auto;"><code>.venv/bin/activate       # (macOS/Linux)</code></pre>
        </li>
        <li>Instalar dependencias:<br>
            <pre style="background-color: #333; color: white; padding: 10px; overflow-x: auto;"><code>pip install -r requirements.txt</code></pre>
        </li>
        <li>Ejecutar servidor (usando Uvicorn):<br>
            <pre style="background-color: #333; color: white; padding: 10px; overflow-x: auto;"><code>uvicorn main:app --reload</code></pre>
        </li>
    </ol>

    <p>Aplicación disponible en: <a href="http://127.0.0.1:8000">http://127.0.0.1:8000</a></p>

    <hr>

    <h2>Endpoints Principales</h2>

    <h3>Análisis (Analytics)</h3>
    <table border="1" style="border-collapse: collapse; width: 100%;">
        <thead>
            <tr><th>Método</th><th>Endpoint</th><th>Descripción</th></tr>
        </thead>
        <tbody>
            <tr><td><code>GET</code></td><td><code>/analisis/</code></td><td>Listar todos los análisis activos.</td></tr>
            <tr><td><code>GET</code></td><td><code>/analisis/new</code></td><td>Muestra el formulario para crear un nuevo análisis.</td></tr>
            <tr><td><code>POST</code></td><td><code>/analisis/new</code></td><td>Crea un nuevo análisis.</td></tr>
            <tr><td><code>GET</code></td><td><code>/analisis/{id}/edit</code></td><td>Muestra el formulario de edición de un análisis.</td></tr>
            <tr><td><code>PATCH</code></td><td><code>/analisis/{id}/desactivar</code></td><td>Desactiva un análisis específico.</td></tr>
        </tbody>
    </table>

    <h3>Metodologías (Methodologies)</h3>
    <table border="1" style="border-collapse: collapse; width: 100%;">
        <thead>
            <tr><th>Método</th><th>Endpoint</th><th>Descripción</th></tr>
        </thead>
        <tbody>
            <tr><td><code>GET</code></td><td><code>/metodologias/</code></td><td>Listar todas las metodologías activas.</td></tr>
            <tr><td><code>GET</code></td><td><code>/metodologia/new</code></td><td>Muestra el formulario para crear una nueva metodología.</td></tr>
            <tr><td><code>PATCH</code></td><td><code>/metodologia/{id}/desactivar</code></td><td>Desactiva una metodología.</td></tr>
        </tbody>
    </table>

    <h3>Usuarios (Users)</h3>
    <table border="1" style="border-collapse: collapse; width: 100%;">
        <thead>
            <tr><th>Método</th><th>Endpoint</th><th>Descripción</th></tr>
        </thead>
        <tbody>
            <tr><td><code>GET</code></td><td><code>/users/</code></td><td>Listar todos los usuarios activos.</td></tr>
            <tr><td><code>GET</code></td><td><code>/users/new</code></td><td>Muestra el formulario para crear un nuevo usuario.</td></tr>
            <tr><td><code>PATCH</code></td><td><code>/users/{id}/desactivar</code></td><td>Desactiva una cuenta de usuario.</td></tr>
        </tbody>
    </table>

    <hr>

    <h2>Convención de Vistas (Jinja2)</h2>
    <p>Todas las vistas heredan la estructura base del proyecto para mantener la consistencia del layout, la navegación y los scripts:</p>
    <pre style="background-color: #eee; padding: 10px; border: 1px solid #ccc; overflow-x: auto;"><code>{% extends 'header.html' %}

{% set title = 'Mi Título Específico' %}

{% block content %}
    &lt;!-- Aquí va el HTML único de esta página --&gt;
{% endblock %}</code></pre>

</body>
</html>
