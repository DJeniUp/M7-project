from django.views.generic import FormView
from django.contrib import messages
from django.shortcuts import redirect

from .forms import ScheduleForm
from .services.csv_bootstrap_service import CsvBootstrapService
from .services.external_scheduler_service import ExternalSchedulerService
from .services.scheduler_service import SchedulerService


class ScheduleView(FormView):
    template_name = 'core/schedule.html'
    form_class = ScheduleForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault('schedule', None)
        context.setdefault('error', None)
        return context

    def form_valid(self, form):
        algorithm = form.cleaned_data['algorithm']
        modules_count = form.cleaned_data['modules_count']
        max_courses_per_module = form.cleaned_data['max_courses_per_module']

        try:
            if algorithm == 'external':
                schedule = ExternalSchedulerService.generate_schedule(
                    modules_count=modules_count,
                    max_courses_per_module=max_courses_per_module,
                )
            else:
                schedule = SchedulerService.generate_schedule(
                    modules_count=modules_count,
                    max_courses_per_module=max_courses_per_module,
                )
        except ValueError as exc:
            return self.render_to_response(
                self.get_context_data(form=form, schedule=None, error=str(exc))
            )

        return self.render_to_response(self.get_context_data(form=form, schedule=schedule, error=None))


schedule_view = ScheduleView.as_view()


def load_csv_data_view(request):
    if request.method != 'POST':
        return redirect('core:schedule')

    try:
        result = CsvBootstrapService.load_from_external_csvs()
    except ValueError as exc:
        messages.error(request, str(exc))
    else:
        messages.success(
            request,
            (
                f"CSV data loaded: {result['teachers']} teachers, {result['courses']} courses. "
                f"Defaults set to modules={result['modules']} and max courses={result['max_courses_per_module']}."
            ),
        )

    return redirect('core:schedule')
