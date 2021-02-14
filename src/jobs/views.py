from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db import transaction
from django.shortcuts import get_object_or_404

from utils.views import AbstractView, AbstractLoginRequiredMixin
from activities.services import create_view_log

from .models import Job
from .forms import JobForm


class JobListView(AbstractLoginRequiredMixin, AbstractView, ListView):
    """
    List of jobs
    """
    template_name = 'jobs/list.html'
    header = _("Job List")
    model = Job
    pagination = True
    enabled_ordering = True

    def get_context_data(self, **kwargs):
        jobs = Job.objects.all()

        search = self.request.GET.get('search', None)
        if search:
            jobs = jobs.filter(title__icontains=search)

        kwargs['objects'] = jobs
        kwargs['search'] = search

        context = super().get_context_data(**kwargs)

        # Log everytime user access this page
        if self.request.user.is_authenticated:
            create_view_log(
                user=self.request.user,
                page="Job"
            )

        return context


class JobDetailView(AbstractLoginRequiredMixin, AbstractView, DetailView):
    """
    Job detail page
    """
    template_name = 'jobs/detail.html'
    header = _("Job")
    pk_url_kwarg = 'uuid'
    model = Job
    context_object_name = 'object'


class JobCreateView(AbstractLoginRequiredMixin, AbstractView, CreateView):
    """
    Create new Job
    """
    template_name = 'jobs/form.html'
    header = _("Add New Job")
    model = Job
    form_class = JobForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['cancel_url'] = reverse('jobs:list')

        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            self.object = form.save()
            transaction.savepoint_commit(sid)
            messages.success(self.request, "Successfull create.")
        except Exception as err:
            print(f"ERROR Create: {err}")
            transaction.savepoint_rollback(sid)
            messages.warning(self.request, "Fail to save the form. Please try again.")
            return self.render_to_response(self.get_context_data(form=form))

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('jobs:detail', kwargs={'uuid': self.object.pk})


class JobUpdateView(AbstractLoginRequiredMixin, AbstractView, UpdateView):
    """
    Update Job
    """
    template_name = 'jobs/form.html'
    header = _("Update Job")
    model = Job
    form_class = JobForm
    pk_url_kwarg = 'uuid'

    def get_object(self):
        return get_object_or_404(Job, pk=self.kwargs[self.pk_url_kwarg])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['cancel_url'] = reverse('jobs:detail', kwargs={'uuid': self.object.pk})
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
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
        return reverse('jobs:detail', kwargs={'uuid': self.object.pk})
