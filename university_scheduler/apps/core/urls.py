from django.urls import path

from .views import load_csv_data_view, schedule_view

app_name = 'core'

urlpatterns = [
    path('', schedule_view, name='schedule'),
    path('load-csv-data/', load_csv_data_view, name='load_csv_data'),
]
