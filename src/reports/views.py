from django.views.generic import View
from django.http import JsonResponse

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
                ('ID', 12),
                ('Name', 40),
                ('DOB', 10),
                ('Job Title', 40),
                ('Salary', 12),
            ]

            data = []

            for employee in employees:
                row = [
                    (str(employee.pk), 'Normal'),
                    (employee.name, 'Normal'),
                    (employee.dob.strftime("%d-%m-%Y"), 'Normal'),
                    (employee.job.title, 'Normal'),
                    (str(employee.salary), 'Normal'),
                ]
                data.append(row)

            workbook = export_to_xlsx("Employee", columns, data)
            status = "SUCCESS"
            export_link = workbook
        except Exception as err:
            print("ERROR import ", err)
            status = "FAIL"
            export_link = None

        response = {
            'status': status,
            'export_link': export_link
        }

        return JsonResponse(response)
