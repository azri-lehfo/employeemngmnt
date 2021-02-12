from django.views.generic import ListView
from django.utils.translation import gettext_lazy as _

from utils.views import AbstractView

from .models import Job


class JobListView(AbstractView, ListView):
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
        ordering = self.request.GET.get('ordering', 'latest')
        if ordering == 'oldest':
            jobs = jobs.order_by('created_at')
        kwargs['objects'] = jobs

        context = super().get_context_data(**kwargs)

        context['ordering'] = ordering
        return context
