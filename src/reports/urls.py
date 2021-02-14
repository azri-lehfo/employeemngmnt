from django.urls import path

from .views import (
    EmployeeExportView,
)


app_name = 'reports'

urlpatterns = [
    path('employees/', EmployeeExportView.as_view(), name='employees'),
    path('jobs/', EmployeeExportView.as_view(), name='jobs'),
]
