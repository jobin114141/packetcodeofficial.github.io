from django.urls import path
from .import views 
from .views import inspect_car

urlpatterns = [
    path("i_reg",views.i_reg,name='i_reg'),
    path("i_mainpage",views.i_mainpage,name='i_mainpage'),  
    path('inspect/<int:car_id>/', inspect_car, name='inspect_car'),    
]

