from django import forms


class ScheduleForm(forms.Form):
    ALGORITHM_CHOICES = (
        ('internal', 'Internal Algorithm'),
        ('external', 'External Algorithm'),
    )

    algorithm = forms.ChoiceField(choices=ALGORITHM_CHOICES, initial='internal')
    modules_count = forms.IntegerField(min_value=1, max_value=20, initial=14)
    max_courses_per_module = forms.IntegerField(min_value=1, max_value=100, initial=9)
