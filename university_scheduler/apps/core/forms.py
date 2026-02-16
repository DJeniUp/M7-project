from django import forms


class ScheduleForm(forms.Form):
    modules_count = forms.IntegerField(min_value=1, max_value=20, initial=6)
    max_courses_per_module = forms.IntegerField(min_value=1, max_value=100, initial=4)
