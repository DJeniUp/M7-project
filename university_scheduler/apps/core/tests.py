from __future__ import annotations

from unittest.mock import patch

from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from apps.core.forms import ScheduleForm
from apps.core.models import Course, Module, Teacher
from apps.core.services.csv_bootstrap_service import CsvBootstrapService


class ScheduleFormTests(TestCase):
    def test_defaults_match_expected_constraints(self):
        form = ScheduleForm()
        self.assertEqual(form.fields['modules_count'].initial, 14)
        self.assertEqual(form.fields['max_courses_per_module'].initial, 9)


class CsvBootstrapServiceTests(TestCase):
    def test_load_from_external_csvs_populates_core_entities(self):
        result = CsvBootstrapService.load_from_external_csvs()

        self.assertEqual(result['modules'], 14)
        self.assertEqual(result['max_courses_per_module'], 9)
        self.assertGreater(result['teachers'], 0)
        self.assertGreater(result['courses'], 0)

        self.assertEqual(Module.objects.count(), 14)
        self.assertEqual(
            list(Module.objects.order_by('number').values_list('number', flat=True)),
            list(range(1, 15)),
        )

        teacher = Teacher.objects.get(name='Abdullah Al-Shaksy')
        self.assertNotIn(11, set(teacher.available_modules.values_list('number', flat=True)))
        self.assertNotIn(12, set(teacher.available_modules.values_list('number', flat=True)))

        course = Course.objects.get(name='Intro to Programming 2: Python')
        prereq_names = set(course.prerequisites.values_list('name', flat=True))
        self.assertIn('Intro to Programming 1: Python', prereq_names)


class LoadCsvDataViewTests(TestCase):
    def test_get_redirects_to_schedule(self):
        response = self.client.get(reverse('core:load_csv_data'))
        self.assertRedirects(response, reverse('core:schedule'))

    @patch('apps.core.views.CsvBootstrapService.load_from_external_csvs')
    def test_post_success_sets_success_message(self, bootstrap_mock):
        bootstrap_mock.return_value = {
            'teachers': 2,
            'courses': 3,
            'modules': 14,
            'max_courses_per_module': 9,
        }

        response = self.client.post(reverse('core:load_csv_data'), follow=True)
        self.assertEqual(response.status_code, 200)

        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertTrue(any('CSV data loaded: 2 teachers, 3 courses' in message for message in messages))

    @patch('apps.core.views.CsvBootstrapService.load_from_external_csvs')
    def test_post_error_sets_error_message(self, bootstrap_mock):
        bootstrap_mock.side_effect = ValueError('CSV files not found')

        response = self.client.post(reverse('core:load_csv_data'), follow=True)
        self.assertEqual(response.status_code, 200)

        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn('CSV files not found', messages)
