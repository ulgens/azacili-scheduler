from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from schedule.models import Program, Section
from braces.views import AnonymousRequiredMixin

import json


class LoginView(AnonymousRequiredMixin, TemplateView):
    template_name = "login.html"
    authenticated_redirect_url = "scheduler"


class SchedulerView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"
    program_list = [{"id": p.id, "kod": p.code} for p in Program.objects.all()]
    extra_context = {"programs": program_list}
