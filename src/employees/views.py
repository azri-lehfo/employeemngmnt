from django.views.generic import ListView
from django.utils.translation import gettext_lazy as _

from utils.views import AbstractView

from .models import Employee


class EmployeeListView(AbstractView, ListView):
    """
    List of employees
    """
    template_name = 'employees/list.html'
    header = _("Employee List")
    model = Employee
    pagination = True
    enabled_ordering = True

    def get_context_data(self, **kwargs):
        employees = Employee.objects.all()
        ordering = self.request.GET.get('ordering', 'latest')
        if ordering == 'oldest':
            employees = employees.order_by('created_at')
        kwargs['objects'] = employees

        context = super().get_context_data(**kwargs)

        context['ordering'] = ordering
        return context
