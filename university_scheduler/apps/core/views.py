from django.views.generic import FormView

from .forms import ScheduleForm
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
        modules_count = form.cleaned_data['modules_count']
        max_courses_per_module = form.cleaned_data['max_courses_per_module']

        try:
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
