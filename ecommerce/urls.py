"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include

# from django.views.generic import TemplateView

urlpatterns = [
    # path('', TemplateView.as_view(template_name='login/login.html')),
    path('jet/', include('jet.urls')),
    path('jet/dashboaard', include('jet.dashboard.urls','jet-dashboard')),
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('admin_tools_stats/', include('admin_tools_stats.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    #google and facebook sign in url
    # path('accounts/', include('allauth.urls')),
    # path('/', include("users.urls")),
    path("__reload__/", include("django_browser_reload.urls")),
    # path('', include("main.urls")),
]
