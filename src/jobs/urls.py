from django.urls import path

from .views import (
    JobListView, JobDetailView, JobCreateView,
    JobUpdateView
)


app_name = 'jobs'

urlpatterns = [
    path('', JobListView.as_view(), name='list'),
    path('<uuid:uuid>/', JobDetailView.as_view(), name='detail'),
    path('create/', JobCreateView.as_view(), name='create'),
    path('edit/<uuid:uuid>/', JobUpdateView.as_view(), name='edit'),
]
