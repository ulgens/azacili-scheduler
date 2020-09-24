import json

from braces.views import AnonymousRequiredMixin
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from schedule.models import Program, Section


class LoginView(AnonymousRequiredMixin, TemplateView):
    template_name = "login.html"
    authenticated_redirect_url = "scheduler"


class SchedulerView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        user = self.request.user

        program_list = [{"id": p.id, "kod": p.code} for p in Program.objects.all()]

        registered_sections = user.sections.filter(
            course__term=settings.ACTIVE_TERM,
        ).select_related(
            "course",
        )

        ctx = super().get_context_data(**kwargs)

        ctx["programs"] = program_list
        ctx["registered_sections"] = registered_sections

        return ctx


@method_decorator(csrf_exempt)
def save_courses(request):
    user = request.user

    sections = json.loads(request.POST["selected_crns"])
    sections = filter(lambda x: x != "-", sections)
    sections = map(int, sections)
    sections = Section.objects.filter(code__in=sections)

    user.sections.clear()
    user.sections.add(*sections)

    return HttpResponse()
