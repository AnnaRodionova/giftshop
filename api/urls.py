from django.urls import path
from api import views

urlpatterns = [
    path('imports', views.import_list, name='import-list'),
    path('imports/<int:import_id>/citizens/<int:citizen_id>', views.citizen, name='citizen'),
    path('imports/<int:import_id>/citizens', views.citizen_list, name='citizen-list'),
    path('imports/<int:import_id>/citizens/birthdays', views.birthdays, name='birthdays'),
    path('imports/<int:import_id>/towns/stat/percentile/age', views.age_percentile, name='age-percentile'),
]
