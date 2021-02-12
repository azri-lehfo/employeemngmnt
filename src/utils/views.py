from django.core.paginator import Paginator
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _


class AbstractView(object):
    header = ""
    pagination = False
    enabled_ordering = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = self.header

        # to use pagination, make sure context recipes is added before super
        if self.pagination and kwargs.get('objects'):
            paginator = Paginator(kwargs['objects'], settings.PAGINATION)
            page_number = self.request.GET.get('page')
            context['pages'] = paginator.get_page(page_number)

        context['enabled_ordering'] = self.enabled_ordering
        return context


class AbstractLoginRequiredMixin(LoginRequiredMixin):
    permission_denied_message = _("You have to logged in to access this page.")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request, messages.WARNING,
                                 self.permission_denied_message)
            return self.handle_no_permission()
        return super(AbstractLoginRequiredMixin, self).dispatch(
            request, *args, **kwargs
        )
