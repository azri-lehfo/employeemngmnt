from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db import transaction
from django.shortcuts import get_object_or_404

from utils.views import AbstractView, AbstractLoginRequiredMixin

from .models import Employee
from .forms import EmployeeForm


class EmployeeListView(AbstractLoginRequiredMixin, AbstractView, ListView):
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

        search = self.request.GET.get('search', None)
        if search:
            employees = employees.filter(name__icontains=search)

        ordering = self.request.GET.get('ordering', 'latest')
        if ordering == 'oldest':
            employees = employees.order_by('created_at')

        kwargs['objects'] = employees

        context = super().get_context_data(**kwargs)

        context['ordering'] = ordering
        return context


class EmployeeDetailView(AbstractLoginRequiredMixin, AbstractView, DetailView):
    """
    Employee detail page
    """
    template_name = 'employees/detail.html'
    header = _("Employee")
    pk_url_kwarg = 'uuid'
    model = Employee
    context_object_name = 'object'


class EmployeeCreateView(AbstractLoginRequiredMixin, AbstractView, CreateView):
    """
    Create new Employee
    """
    template_name = 'employees/create.html'
    header = _("Add New Employee")
    model = Employee
    form_class = EmployeeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['cancel_url'] = reverse('employees:list')

        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            self.object = form.save(create=True)
            transaction.savepoint_commit(sid)
            messages.success(self.request, "Successfull create.")
        except Exception as err:
            print(f"ERROR Create: {err}")
            transaction.savepoint_rollback(sid)
            messages.warning(self.request, "Fail to save the form. Please try again.")
            return self.render_to_response(self.get_context_data(form=form))

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('employees:detail', kwargs={'uuid': self.object.pk})


class EmployeeUpdateView(AbstractLoginRequiredMixin, AbstractView, UpdateView):
    """
    Update Employee
    """
    template_name = 'employees/create.html'
    header = _("Update Employee")
    model = Employee
    form_class = EmployeeForm
    pk_url_kwarg = 'uuid'

    def get_object(self):
        return get_object_or_404(Employee, pk=self.kwargs[self.pk_url_kwarg])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['cancel_url'] = reverse('employees:detail', kwargs={'uuid': self.object.pk})
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.warning(self.request, form.errors)
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            form.save()

            transaction.savepoint_commit(sid)
            messages.success(self.request, "Successfull update.")
        except Exception as err:
            print(f"ERROR: {err}")
            transaction.savepoint_rollback(sid)
            messages.warning(self.request, "Fail to save the form. Please try again.")
            return self.render_to_response(self.get_context_data(form=form))

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('employees:detail', kwargs={'uuid': self.object.pk})
