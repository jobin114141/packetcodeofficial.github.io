from django.urls import path
from crain_service import views
urlpatterns = [
    path("crain_main",views.crain_main,name='crain_main'),
    path("Start",views.Start,name='Start'),
    path("payment",views.payment,name='payment'),
    path("craindriver_reg",views.craindriver_reg,name='craindriver_reg'),
]






