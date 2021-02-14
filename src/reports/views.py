from django.views.generic import View
from django.http import HttpResponse

from employees.models import Employee

from .services import export_to_xlsx


class EmployeeExportView(View):
    """
    Export Employee.
    """

    def get(self, request, *args, **kwargs):
        employees = Employee.objects.all()

        search = self.request.GET.get('search', None)
        if search:
            employees = employees.filter(name__icontains=search)

        ordering = self.request.GET.get('ordering', 'latest')
        if ordering == 'oldest':
            employees = employees.order_by('created_at')

        try:
            columns = [
                ('ID', 40),
                ('Name', 40),
                ('DOB', 10),
                ('Job Title', 40),
                ('Salary', 12),
                ('Created At', 10),
            ]

            data = []

            for employee in employees:
                row = [
                    (str(employee.pk), 'Normal'),
                    (employee.name, 'Normal'),
                    (employee.dob.strftime("%d-%m-%Y"), 'Normal'),
                    (employee.job.title, 'Normal'),
                    (str(employee.salary), 'Normal'),
                    (employee.created_at.strftime("%d-%m-%Y"), 'Normal'),
                ]
                data.append(row)

            response = export_to_xlsx("Employee", columns, data)

            return response
        except Exception as err:
            print("ERROR import ", err)

        return HttpResponse("ERROR")
