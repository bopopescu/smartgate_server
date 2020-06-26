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
    path('and_date',views.test_date_send),
    path('check_room_remain', views.remain_room_selected_date),
    path('insert_newbook',views.insert_booklist_reservation),
    path('udp_connection', views.udp_module_code),
    path('get_user_booklist', views.get_user_booklists),
    path('cancel_reservation', views.cancel_reservations),

]
