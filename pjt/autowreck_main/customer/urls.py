from django.urls import path
from .import views 
from.views import c_view_details,sail_closee,generate_pdf
urlpatterns = [
    path("c_mainpage",views.c_mainpage,name='c_mainpage'),  
    path("c_view_details/<int:car_id>/",c_view_details,name='c_view_details'), 
    path("dash_board",views.dash_board,name='dash_board'),
    path("My_history",views.My_history,name='My_history'),
    path('sail_closee/<int:car_id>/pdf/', generate_pdf, name='generate_pdf'),
    path("crain_page",views.crain_page,name='crain_page'), 
    path("crain_booking",views.crain_booking,name='crain_booking'),
    path("crain_status",views.crain_status,name='crain_status'),
    path("completed_crain",views.completed_crain,name='completed_crain'),
        
]