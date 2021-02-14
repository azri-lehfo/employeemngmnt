from django.urls import path

from .views import (
    EmployeeExportView, JobExportView, TrackingExportView
)


app_name = 'reports'

urlpatterns = [
    path('employees/', EmployeeExportView.as_view(), name='employees'),
    path('jobs/', JobExportView.as_view(), name='jobs'),
    path('trackings/', TrackingExportView.as_view(), name='trackings'),
]
