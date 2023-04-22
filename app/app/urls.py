"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from views.views import get_expense_timeseries, get_expense_timeseries_group_by_service, get_expense_timeseries_group_by_mode

urlpatterns = [
    path('admin/', admin.site.urls),
    path('get_expense_timeseries/', get_expense_timeseries, name="get_expense_timeseries"),
    path('get_expense_timeseries_group_by_service/', get_expense_timeseries_group_by_service, name="get_expense_timeseries_group_by_service"),
    path("get_expense_timeseries_group_by_mode/", get_expense_timeseries_group_by_mode, name="get_expense_timeseries_group_by_mode")
]
