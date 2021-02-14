from django.views.generic import View
from django.http import HttpResponse
from django.contrib.auth.models import User

from employees.models import Employee
from jobs.models import Job
from utils.views import AbstractLoginRequiredMixin

from .services import export_to_xlsx


class EmployeeExportView(AbstractLoginRequiredMixin, View):
    """
    Export Employee.
    """

    def get(self, request, *args, **kwargs):
        employees = Employee.objects.all()

        search = self.request.GET.get('search', None)
        if search:
            employees = employees.filter(name__icontains=search)

        try:
            columns = [
                ('ID', 40),
                ('Name', 40),
                ('DOB', 10),
                ('Job Title', 40),
                ('Salary', 12),
                ('Created At', 20),
            ]

            data = []

            for employee in employees:
                row = [
                    (str(employee.pk), 'Normal'),
                    (employee.name, 'Normal'),
                    (employee.dob.strftime("%d-%m-%Y"), 'Normal'),
                    (employee.job.title, 'Normal'),
                    (str(employee.salary), 'Normal'),
                    (employee.created_at.strftime("%d-%m-%Y %H:%M:%S"), 'Normal'),
                ]
                data.append(row)

            response = export_to_xlsx("Employee", columns, data)

            return response
        except Exception as err:
            print("ERROR import ", err)

        return HttpResponse("ERROR")


class JobExportView(AbstractLoginRequiredMixin, View):
    """
    Export Job.
    """

    def get(self, request, *args, **kwargs):
        jobs = Job.objects.all()

        search = self.request.GET.get('search', None)
        if search:
            jobs = jobs.filter(name__icontains=search)

        try:
            columns = [
                ('ID', 40),
                ('Title', 40),
                ('Description', 60),
                ('Min Salary', 12),
                ('Max Salary', 12),
                ('Created At', 20),
            ]

            data = []

            for job in jobs:
                row = [
                    (str(job.pk), 'Normal'),
                    (job.title, 'Normal'),
                    (job.description, 'Normal'),
                    (str(job.min_salary), 'Normal'),
                    (str(job.max_salary), 'Normal'),
                    (job.created_at.strftime("%d-%m-%Y %H:%M:%S"), 'Normal'),
                ]
                data.append(row)

            response = export_to_xlsx("Job", columns, data)

            return response
        except Exception as err:
            print("ERROR import ", err)

        return HttpResponse("ERROR")


class TrackingExportView(AbstractLoginRequiredMixin, View):
    """
    Export Tracking.
    """

    def get(self, request, *args, **kwargs):
        users = User.objects.all()

        try:
            columns = [
                ('Email', 30),
                ('Access Times', 12),
                ('Page', 20),
            ]

            data = []
            pages = ["Employee", "Job"]

            for user in users:
                for page in pages:
                    if user.log_set.filter(page=page).exists():
                        row = [
                            (user.email, 'Normal'),
                            (user.log_set.filter(page=page).count(), 'Normal'),
                            (page, 'Normal'),
                        ]
                        data.append(row)

            response = export_to_xlsx("Tracking", columns, data)

            return response
        except Exception as err:
            print("ERROR import ", err)

        return HttpResponse("ERROR")
