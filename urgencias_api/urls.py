"""
URL configuration for urgencias_api project.

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
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from urgencias import views
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('usuarios_json', views.obtenerUsuarios),
    # path('formularios_json', views.obtenerFormularios),

    path('formularios/', views.formularios_list),
    path('formularios/<int:id>', views.formulario_detail),
    path('formularios/crear/', views.formularios_create),
    path('login/', views.login),
    path('historial/', views.historial),
    path('logout/', views.logout),
    path('', TemplateView.as_view(template_name='index.html')),

] 


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

