# Sistema de Gestión de Maquinaria – Backend
Backend corporativo para la gestión integral de maquinaria, mantenimiento preventivo y control operativo, desarrollado con Python y Django Rest Framework, enfocado en escalabilidad, seguridad, trazabilidad y control por roles.

Este sistema modela escenarios reales del sector industrial, permitiendo a las organizaciones reducir fallos operativos, anticipar mantenimientos y garantizar la trazabilidad técnica de sus activos.

## Visión Técnica
El backend fue diseñado bajo principios de arquitectura limpia, separación de responsabilidades y control de acceso estricto, integrando:
* Autenticación segura con JWT
* Control granular de permisos por rol
* Lógica de negocio desacoplada de la capa de presentación
* Persistencia confiable con PostgreSQL
* Automatización de alertas y contadores de mantenimiento
* Preparación para entornos productivos en la nube

## Problemática que Resuelve
En muchas organizaciones industriales:
* El mantenimiento se gestiona de forma reactiva.
* No existe trazabilidad real por máquina o componente.
* Las horas de uso no se controlan correctamente.
* No hay alertas tempranas de fallos.

Este backend centraliza, automatiza y controla todo el ciclo de vida operativo de la maquinaria.

## Funcionalidades Clave

### Gestión Avanzada de Roles
* Administrador de configuración
* Responsable de mantenimiento
* Operador
* Técnico de mantenimiento

Cada rol tiene permisos explícitos definidos a nivel de endpoint y acción.

### Gestión de Activos
* Registro de empresas, proyectos y maquinarias.
* Identificación única de cada máquina.
* Asociación de máquinas a proyectos con control de horas pactadas.
* Bloqueo automático al completar las horas asignadas.

### Mantenimiento Preventivo
* Definición de planes de mantenimiento por máquina y componente.
* Periodicidad basada en horas de uso reales.
* Ejecución de mantenimientos con:
    * Fecha
    * Responsable
    * Actividades realizadas
    * Insumos y repuestos utilizados
    * Evidencias fotográficas

### Control Diario de Operación
* Registro diario de horas trabajadas por máquina.
* Captura de:
    * Horómetro inicial y final
    * Operador
    * Proyecto
    * Evidencias (planillas y fotos)

### Alertas Automáticas
* Alertas cuando un mantenimiento está próximo a vencerse.
* Alertas cuando el mantenimiento ya está vencido.
* Panel de estado general de maquinaria:
    * En operación
    * Pendientes
    * Vencidas
    * Al día

### Trazabilidad y Auditoría
* Histórico completo de mantenimientos.
* Seguimiento por máquina y componente.
* Actualización automática de updated_at mediante triggers en base de datos.

## Arquitectura del Backend
El sistema está estructurado por dominios funcionales, no por capas técnicas genéricas.

### Estructura Modular
/modulo/
 ├── models/         → Entidades del dominio
 ├── repositories/   → Acceso a datos
 ├── services/       → Lógica de negocio
 ├── serializers/    → Validación y transformación
 ├── views/          → Exposición de la API
 ├── urls.py
 └── signals.py      → Automatizaciones (usuarios y logins)

### Beneficios:
* Código desacoplado
* Alta mantenibilidad
* Facilidad para escalar
* Testing más sencillo
* Claridad para equipos de desarrollo

## Módulos del Sistema
* Usuarios & Logins – Gestión de credenciales y perfiles.
* Empresas & Proyectos – Organización operativa.
* Maquinarias – Gestión de activos físicos.
* Hojas de Vida – Historial técnico documental por máquina.
* Mantenimientos Programados – Planificación preventiva.
* Mantenimientos – Ejecución y registro técnico.
* Registro de Horas – Control operativo diario.
* Alarmas – Sistema automático de alertas.
* Conductores & Cursos – Cumplimiento normativo y formación.

## Seguridad y Control de Acceso
* Autenticación con JWT (SimpleJWT).
* Autorización basada en permisos explícitos por acción (list, create, update, etc.).
* Protección de endpoints sensibles.
* Configuración de CORS para integración frontend segura.

## Persistencia de Datos
* PostgreSQL como motor de base de datos.
* ORM de Django para consistencia y seguridad.
* Triggers SQL para mantener campos de auditoría actualizados.
* Base de datos desplegada en entorno cloud.

## Despliegue en Producción
* Plataforma: Render
* Servidor: Gunicorn
* Base de datos: PostgreSQL
* Backend accesible públicamente: https://gestion-maquinaria-backend.onrender.com

## Stack Tecnológico
* Backend: Python, Django, Django Rest Framework
* Seguridad: JWT, CORS
* Base de datos: PostgreSQL
* Despliegue: Render
* Control de versiones: Git & GitHub
* Arquitectura: Modular, orientada a dominio

## Instalación Local
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

## Credenciales Iniciales (Solo Desarrollo)
{
  "username": "admin_servimacons",
  "password": "admin123*"
}

## Repositorio
https://github.com/Stivenpaez09/gestion-maquinaria-backend

## Autor
Stiven Páez
Backend Developer
Python · Django Rest Framework · PostgreSQL · Arquitectura Backend













