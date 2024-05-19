from django.urls import path 
from .views import ChargeStationAPIView, TempDataAPIView


urlpattern = [
    # path('api/ChargeStationINFO', ChargeStationAPIView.as_view(), name='chargestaion_info_api'),
    path ('api/tempData', TempDataAPIView.as_view(), name='temp_data_api'),
]