from django.contrib import admin
from .models import Department, CustomUser, HOD, Staff, Admin, Attendance, LeaveRequest, LeaveReportHOD, LeaveReportStaff, FeedBackHOD, FeedBackStaff, NotificationHOD, NotificationStaff

# Register your models here

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'department_name')
    search_fields = ('department_name',)

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'user_type')
    search_fields = ('username', 'email')
    list_filter = ('user_type',)

@admin.register(HOD)
class HODAdmin(admin.ModelAdmin):
    list_display = ('id', 'admin', 'department', 'gender', 'created_at', 'updated_at')
    search_fields = ('admin__username', 'department__department_name')
    list_filter = ('department', 'gender')

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('id', 'admin', 'department', 'position', 'created_at', 'updated_at')
    search_fields = ('admin__username', 'position', 'department__department_name')
    list_filter = ('department', 'position')

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('id', 'admin', 'created_at', 'updated_at')
    search_fields = ('admin__username',)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'staff', 'hod', 'attendance_date', 'clock_in', 'clock_out', 'status', 'created_at', 'updated_at')
    search_fields = ('staff__admin__username', 'hod__admin__username', 'attendance_date')
    list_filter = ('status',)

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'leave_date', 'leave_message', 'status', 'created_at', 'updated_at')
    search_fields = ('user__username', 'leave_date')
    list_filter = ('status',)

@admin.register(LeaveReportHOD)
class LeaveReportHODAdmin(admin.ModelAdmin):
    list_display = ('id', 'hod_id', 'leave_date', 'leave_message', 'leave_status', 'created_at', 'updated_at')
    search_fields = ('hod_id__admin__username', 'leave_date')
    list_filter = ('leave_status',)

@admin.register(LeaveReportStaff)
class LeaveReportStaffAdmin(admin.ModelAdmin):
    list_display = ('id', 'staff_id', 'leave_date', 'leave_message', 'leave_status', 'created_at', 'updated_at')
    search_fields = ('staff_id__admin__username', 'leave_date')
    list_filter = ('leave_status',)

@admin.register(FeedBackHOD)
class FeedBackHODAdmin(admin.ModelAdmin):
    list_display = ('id', 'hod_id', 'feedback', 'feedback_reply', 'created_at', 'updated_at')
    search_fields = ('hod_id__admin__username',)
    list_filter = ('created_at',)

@admin.register(FeedBackStaff)
class FeedBackStaffAdmin(admin.ModelAdmin):
    list_display = ('id', 'staff_id', 'feedback', 'feedback_reply', 'created_at', 'updated_at')
    search_fields = ('staff_id__admin__username',)
    list_filter = ('created_at',)

@admin.register(NotificationHOD)
class NotificationHODAdmin(admin.ModelAdmin):
    list_display = ('id', 'hod_id', 'message', 'created_at', 'updated_at')
    search_fields = ('hod_id__admin__username',)
    list_filter = ('created_at',)

@admin.register(NotificationStaff)
class NotificationStaffAdmin(admin.ModelAdmin):
    list_display = ('id', 'staff_id', 'message', 'created_at', 'updated_at')
    search_fields = ('staff_id__admin__username',)
    list_filter = ('created_at',)

