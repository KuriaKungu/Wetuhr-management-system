from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from hr_management_system import settings
from django.views.decorators.csrf import csrf_exempt
from hr import hodviews, staffviews, adminviews, views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('accounts/', include('django.contrib.auth.urls')),
    # path('', views.showLoginPage, name="show_login"),
    # path('doLogin/', views.doLogin, name='do_login'),
    # path('demo/', views.showDemoPage),
    # path('get_user_details/', views.GetUserDetails, name='get_user_details'),
    # path('logout_user/', views.logout_User, name='logout_user'),

    path('admin/', admin.site.urls),
    path('', views.showLoginPage, name="show_login"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('doLogin/', views.doLogin, name='do_login'),
    path('logout_user/', views.logout_User, name='logout_user'),
    path('admin_home/', adminviews.admin_home, name='admin_home'),
    path('hod_home/', hodviews.hod_home, name='hod_home'),
    path('staff_home/', staffviews.staff_home, name='staff_home'),
    path('get_user_details/', views.GetUserDetails, name='get_user_details'),


    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Admin URL Paths
    path('admin_home/', adminviews.admin_home, name='admin_home'),
    path('add_hod/', adminviews.add_hod, name='add_hod'),
    # path('add_hod_save/', adminviews.add_hod_save, name='add_hod_save'),
    path('manage_hod/', adminviews.manage_hod, name='manage_hod'),
    path('edit_hod/<str:hod_id>/', adminviews.edit_hod, name='edit_hod'),
    path('view_hod/<str:hod_id>/', adminviews.view_hod, name='view_hod'),
    path('delete_hod/<str:hod_id>/', adminviews.delete_hod, name='delete_hod'),
    # path('edit_hod_save/', adminviews.edit_hod_save, name='edit_hod_save'),
    path('add_staff/', adminviews.add_staff, name='add_staff'),
    # path('add_staff_save/', adminviews.add_staff_save, name='add_staff_save'),
    path('manage_staff/', adminviews.manage_staff, name='manage_staff'),
    path('edit_staff/<str:staff_id>/', adminviews.edit_staff, name='edit_staff'),
    path('view_staff/<str:staff_id>/', adminviews.view_staff, name='view_staff'),
    path('delete_staff/<str:staff_id>/', adminviews.delete_staff, name='delete_staff'),
    # path('view_staff/<str:staff_id>/', adminviews.view_staff, name='view_staff'),
    # path('edit_staff_save/', adminviews.edit_staff_save, name='edit_staff_save'),
    path('staff_leave_view/', adminviews.staff_leave_view, name='staff_leave_view'),
    path('hod_apply_leave_view/', adminviews.hod_leave_view, name='hod_leave_view'),
    path('admin_view_hod_attendance/', adminviews.admin_view_hod_attendance, name='admin_view_hod_attendance'),
    # path('admin_view_staff_attendance/', adminviews.admin_view_staff_attendance, name='admin_view_staff_attendance'),
    # path('admin_get_attendance_dates/', adminviews.admin_get_attendance_dates, name='admin_get_attendance_dates'),
    path('admin_view_hod_attendance/', adminviews.admin_view_hod_attendance, name='admin_view_hod_attendance'),
    path('admin_view_staff_attendance/', adminviews.admin_view_staff_attendance, name='admin_view_staff_attendance'),
    path('admin_send_notification_hod/', adminviews.admin_send_notification_hod, name='admin_send_notification_hod'),
    path('admin_send_notification_staff/', adminviews.admin_send_notification_staff, name='admin_send_notification_staff'),
    path('send_hod_notification',adminviews.send_hod_notification,name="send_hod_notification"),
    path('send_staff_notification',adminviews.send_staff_notification,name="send_staff_notification"),
    path('add_department/', adminviews.add_department, name='add_department'),

    path('add_department/', adminviews.add_department, name='add_department'),


    # path('add_department_save/', adminviews.add_department_save, name='add_department_save'),

    path('manage_department/', adminviews.manage_department, name='manage_department'),
    path('edit_department/<str:department_id>/', adminviews.edit_department, name='edit_department'),
    path('view_department/<str:department_id>/', adminviews.view_department, name='view_department'),
    path('delete_department/<str:department_id>/', adminviews.delete_department, name='delete_department'),

    # path('edit_department/', adminviews.edit_department, name='edit_department'),
    # path('edit_department_save/', adminviews.edit_department_save, name='edit_department_save'),
    path('edit_department/<int:department_id>/', adminviews.edit_department, name='edit_department'),
    path('admin_profile', adminviews.admin_profile, name="admin_profile"),
    path('admin_profile_save', adminviews.admin_profile_save,name="admin_profile_save"),
    path('check_email_exist',adminviews.check_email_exist,name="check_email_exist"),
    path('check_username_exist',adminviews.check_username_exist,name="check_username_exist"),
    path('hod_feedback_message',adminviews.hod_feedback_message,name="hod_feedback_message"),
    path('hod_feedback_message_replied',adminviews.hod_feedback_message_replied,name="hod_feedback_message_replied"),
    path('staff_feedback_message',adminviews.staff_feedback_message,name="staff_feedback_message"),
    path('staff_feedback_message_replied',adminviews.staff_feedback_message_replied,name="staff_feedback_message_replied"),

    # Staff Leave Management
    path('staff_leave/', adminviews.staff_leave_view, name='staff_leave_view'),
    path('staff_leave/approve/<int:leave_id>/', adminviews.staff_approve_leave, name='staff_approve_leave'),
    path('staff_leave/disapprove/<int:leave_id>/', adminviews.staff_disapprove_leave, name='staff_disapprove_leave'),

    # HOD Leave Management
    path('hod_leave/', adminviews.hod_leave_view, name='hod_leave_view'),
    path('hod_leave/approve/<int:leave_id>/', adminviews.hod_approve_leave, name='hod_approve_leave'),
    path('hod_leave/disapprove/<int:leave_id>/', adminviews.hod_disapprove_leave, name='hod_disapprove_leave'),


    #HOD URL Paths
    path('hod_profile/', hodviews.hod_profile, name='hod_profile'),
    path('hod_home/', hodviews.hod_home, name='hod_home'),
    path('hod_manage_staff/', hodviews.manage_staff, name='hod_manage_staff'),
    path('edit_staff/<int:staff_id>/', hodviews.edit_staff, name='hod_edit_staff'),
    path('hod_take_attendance/', hodviews.hod_take_attendance, name='hod_take_attendance'),
    # path('hod/hod_view_staff_attendance/', hodviews.hod_view_staff_attendance, name='hod_view_staff_attendance'),
    path('hod_attendance_records/', hodviews.hod_attendance_records, name='hod_attendance_records'),
    path('hod_all_notification',hodviews.hod_all_notification,name="hod_all_notification"),
    # path('view_attendance/', views.view_attendance, name='view_attendance'),
    # path('hod_feedback_message/', views.hod_feedback_message, name='hod_feedback_message'),
    path('hod_apply_leave/', hodviews.hod_apply_leave, name='hod_apply_leave'),
    path('hod_feedback', hodviews.hod_feedback, name='hod_feedback'),
    # path('hod_feedback_save', hodviews.hod_feedback_save, name=hod_feedback_save),
    # path('hod_send_notification/', views.hod_send_notification, name='hod_send_notification'),
    path('hod_fcmtoken_save', hodviews.hod_fcmtoken_save,name="hod_fcmtoken_save"),
    

    #Staff URL Paths
    path('staff_home/', staffviews.staff_home, name='staff_home'),
    path('staff_take_attendance/', staffviews.staff_take_attendance, name='staff_take_attendance'),
    path('attendance_records/', staffviews.staff_attendance_records, name='staff_attendance_records'),
    path('get_staff/', staffviews.get_staff, name='get_staff'),
    path('staff_all_notification',staffviews.staff_all_notification,name="staff_all_notification"),
    path("staff_apply_leave", staffviews.staff_apply_leave, name="staff_apply_leave"),
    # path("staff_apply_leave_save", staffviews.staff_apply_leave_save, name="staff_apply_leave_save"),
    path("staff_feedback", staffviews.staff_feedback, name="staff_feedback"),
    # path("staff_feedback_save", staffviews.staff_feedback_save, name="staff_feedback_save"),
    path('staff_fcmtoken_save',staffviews.staff_fcmtoken_save,name="staff_fcmtoken_save"),
    path('firebase-messaging-sw.js',views.showFirebaseJS,name="show_firebase_js"),
    
]

# Static and media URL configurations for development mode
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Additional static URL configuration in debug mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
