from django.urls import path
from . import views

urlpatterns = [
    path('get_file_content/<str:file_id>/', views.get_file_content, name='get_file_content'),
    path('load_create_features_object/<str:file_id>/', views.load_create_features_object, name='load_create_features_object'),
    path('rest/services/run_forecast_modelling', views.run_forecast_modelling, name='run_forecast_modelling'),
    path('rest/services/convert_event_to_request_payload/<str:file_id>/', views.convert_event_to_request_payload, name='convert_event_to_request_payload'),
    path('postprocess/generate_forecast_modelling_response', views.generate_forecast_modelling_response, name='generate_forecast_modelling_response'),
    
    # Add other URL patterns if needed
]