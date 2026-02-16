from django.urls import path

from .views import schedule_view

app_name = 'core'

urlpatterns = [
    path('', schedule_view, name='schedule'),
]
