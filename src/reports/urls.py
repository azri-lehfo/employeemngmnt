from django.urls import path

from .views import (
    ReportListView, EmployeeExportView, JobExportView, TrackingExportView
)


app_name = 'reports'

urlpatterns = [
    path('', ReportListView.as_view(), name='list'),
    path('employees/', EmployeeExportView.as_view(), name='employees'),
    path('jobs/', JobExportView.as_view(), name='jobs'),
    path('trackings/', TrackingExportView.as_view(), name='trackings'),
]
