from django.urls import path

from .views import (
    EmployeeListView, EmployeeDetailView, EmployeeCreateView,
    EmployeeUpdateView
)


app_name = 'employees'

urlpatterns = [
    path('', EmployeeListView.as_view(), name='list'),
    path('<uuid:uuid>/', EmployeeDetailView.as_view(), name='detail'),
    path('create/', EmployeeCreateView.as_view(), name='create'),
    path('edit/<uuid:uuid>/', EmployeeUpdateView.as_view(), name='edit'),
]
