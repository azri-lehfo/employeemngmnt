from django.urls import path

from .views import (
    EmployeeExportView,
)


app_name = 'reports'

urlpatterns = [
    path('', EmployeeExportView.as_view(), name='employees'),
]
