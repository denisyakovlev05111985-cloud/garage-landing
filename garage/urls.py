from django.urls import path
from . import views

urlpatterns = [
<<<<<<< Updated upstream
    path("", views.index, name="index"),
]
=======
    path('', views.index, name='index'),
    path('booking/ajax/', views.booking_ajax, name='booking_ajax'),
]
>>>>>>> Stashed changes
