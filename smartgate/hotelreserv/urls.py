from django.urls import path
from . import views

urlpatterns = [
    path('log_in', views.log_in),
    path('check_id', views.dup_check_id),
    path('check_email', views.dup_check_email),
    path('check_tel', views.dup_check_phone),
    path('timetest', views.insert_booked_info),
    path('add_user', views.add_user),
    path('my_book_list', views.my_book_list),
    path('time_now', views.print_time_now),

]
