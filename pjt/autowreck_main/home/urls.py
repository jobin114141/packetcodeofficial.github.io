from django.urls import path
from .import views 
from .views import sail_close
urlpatterns = [
    
    path("c_reg",views.c_reg,name='c_reg'),
    path("",views.home,name='home'),
    path("m_reg",views.m_reg,name='m_reg'),
    path("main_login",views.main_login,name='main_login'),
    path("inactive",views.inactive,name='inactive'),
    path("main_admin",views.main_admin,name='main_admin'),
    path("admin_car_upload",views.admin_car_upload,name='admin_car_upload'),
    path("manager_admin_viewpage",views.manager_admin_viewpage,name='manager_admin_viewpage'),
    path("admin_sail_details",views.admin_sail_details,name='admin_sail_details'),
    path('sail_close/<int:list_id>/', sail_close, name='sail_close'),
    path("All_bids",views.All_bids,name='All_bids'),    
    path("closed_deals",views.closed_deals,name='closed_deals'), 
    path("remove_car",views.remove_car,name='remove_car'), 
    path("crain_delliverd",views.crain_delliverd,name='crain_delliverd'), 
]