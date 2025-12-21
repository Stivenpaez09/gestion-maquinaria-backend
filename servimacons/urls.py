"""
URL configuration for servimacons project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from servimacons import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/usuarios/', include('usuarios.urls')),
    path('api/maquinarias/', include('maquinarias.urls')),
    path('api/conductores/', include('conductores.urls')),
    path('api/empresas/', include('empresas.urls')),
    path('api/cursos/', include('cursos.urls')),
    path('api/proyectos/', include('proyectos.urls')),
    path('api/mantenimientos-programados/', include('mantenimientos_programados.urls')),
    path('api/mantenimientos/', include('mantenimientos.urls')),
    path('api/hojas-vida/', include('hojas_vida.urls')),
    path('api/proyecto-maquinaria/', include('proyecto_maquinaria.urls')),
    path('api/registros-horarios-maquinaria/', include('registros_horas_maquinaria.urls')),
    path('api/alarmas/', include('alarmas.urls')),
    path('api/logins/', include('logins.urls')),
]
