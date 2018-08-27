from django.views.generic import TemplateView

from schedule.models import Program


class IndexView(TemplateView):
    template_name = "index.html"
    program_list = [{"id": p.id, "kod": p.code} for p in Program.objects.all()]
    extra_context = {"programs": program_list}
