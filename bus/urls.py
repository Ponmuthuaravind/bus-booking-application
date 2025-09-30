"""
URL configuration for bus project.

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
from logsign import views as v1
from home import views as v2

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sign/',v1.signView,name = 'sign'),
    path('login/',v1.loginview,name= 'login'),
    path('home/<person>/',v2.homeview,name= 'home'),
    path('book/<bus>/',v2.seatbookview,name='seatbook'),
    path('cancel-ticket/', v2.cancelticket, name='cancelticket'),
    path('view-ticket/', v2.viewticket, name='viewticket'),
    path('recover-ticket/', v2.recoverticket, name='recoverticket'),
    path('cancel/<int:journey_id>/',v2.cancelview,name='cancel'),
    path('download-ticket/<int:ticket_id>/', v2.downloadticket, name='downloadticket'),


]
