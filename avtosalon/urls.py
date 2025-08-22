from django.urls import path
from avtosalon.views import *

urlpatterns = [
    path('', login_views, name='login'),
    path('logout/', logout_view, name='logout'),
    path('/index', index, name='index'),
    path('add_car/', add_car, name='add_car'),
    path("category/<int:pk>/", category, name="category"),
    path('detail_car/<int:pk>/', detail_car, name='detail_car'),
    path("car/<int:pk>/pdf/", car_pdf, name="car_pdf"),
    
]