from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from hr.models import CustomUser
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date, parse_time
from datetime import datetime
from .models import HOD, CustomUser, FeedBackHOD, LeaveReportHOD, NotificationHOD, Staff, Department, Attendance, LeaveRequest
from django.contrib.auth.decorators import login_required





@login_required
def hod_home(request):
    user = request.user
    hod = HOD.objects.get(admin=user)
    department = hod.department

    staff_count = Staff.objects.filter(department=department).count()
    staff_name_list = []
    staff_clock_in_list = []
    staff_clock_out_list = []
    staff_leave_list = []

    hod_clock_in_count = Attendance.objects.filter(hod=hod, clock_in__isnull=False).count()
    hod_clock_out_count = Attendance.objects.filter(hod=hod, clock_out__isnull=False).count()
    hod_leave_count = LeaveRequest.objects.filter(user=hod.admin, status='Approved').count()

    staffs = Staff.objects.filter(department=department)
    for staff in staffs:
        clock_in_count = Attendance.objects.filter(staff=staff, clock_in__isnull=False).count()
        clock_out_count = Attendance.objects.filter(staff=staff, clock_out__isnull=False).count()
        leave_count = LeaveRequest.objects.filter(user=staff.admin, status='Approved').count()
        staff_name_list.append(staff.admin.username)
        staff_clock_in_list.append(clock_in_count)
        staff_clock_out_list.append(clock_out_count)
        staff_leave_list.append(leave_count)

    total_hod_attendance = hod_clock_in_count + hod_clock_out_count
    total_hod_leaves = hod_leave_count

    context = {
        "staff_count": staff_count,
        "department_name": department.department_name,
        "staff_name_list": staff_name_list,
        "staff_clock_in_list": staff_clock_in_list,
        "staff_clock_out_list": staff_clock_out_list,
        "staff_leave_list": staff_leave_list,
        "hod_clock_in_count": hod_clock_in_count,
        "hod_clock_out_count": hod_clock_out_count,
        "hod_leave_count": hod_leave_count,
        "total_hod_attendance": total_hod_attendance,
        "total_hod_leaves": total_hod_leaves,
    }

    return render(request, "hod_template/hod_home_template.html", context)

def hod_profile(request):
     if request.method == "POST":
         first_name = request.POST.get("first_name")
         last_name = request.POST.get("last_name")
         address = request.POST.get("address")
         try:
             customuser = CustomUser.objects.get(id=request.user.id)
             customuser.first_name = first_name
             customuser.last_name = last_name
             customuser.address = address
             customuser.save()

             messages.success(request, "Successfully Updated Profile")
         except Exception as e:
             messages.error(request, f"Failed to Update Profile: {e}")
         return redirect("hod_profile")
    
     else:
         user = CustomUser.objects.get(id=request.user.id)
         return render(
             request,
             "hod_template/hod_profile.html",
             {"user": user},
         )

    
@login_required
def manage_staff(request):
    user = request.user
    hod = HOD.objects.get(admin=user)
    department = hod.department

    staff_list = Staff.objects.filter(department=department)
    # staff_list = Staff.objects.all()
    return render(request, 'hod_template/manage_staff_template.html', {'staff_list': staff_list})
# @login_required
# def manage_staff(request):
#     if request.user.user_type != 2:  # Check if the user is an HOD
#         return HttpResponseForbidden("You are not authorized to view this page.")
    
#     hod = get_object_or_404(HOD, admin=request.user)
#     staff_list = Staff.objects.filter(department=hod.department)
    
#     context = {
#         'staff_list': staff_list
#     }
#     return render(request, 'hod_template/manage_staff.html', context)


# class InlineStaffForm(forms.ModelForm):
#     class Meta:
#         model = CustomUser
#         fields = ['email', 'first_name', 'last_name', 'address']

# class InlineStaffProfileForm(forms.ModelForm):
#     class Meta:
#         model = Staff
#         fields = ['address', 'gender', 'position']

# @login_required
# def edit_staff(request, staff_id):
#     if request.user.user_type != 2:  # Check if the user is an HOD
#         return HttpResponseForbidden("You are not authorized to view this page.")
    
#     hod = get_object_or_404(HOD, admin=request.user)
#     staff_user = get_object_or_404(CustomUser, id=staff_id)
#     staff_profile = get_object_or_404(Staff, admin=staff_user)

#     if staff_profile.department != hod.department:
#         return HttpResponseForbidden("You are not authorized to edit this staff member.")
    
#     if request.method == 'POST':
#         user_form = InlineStaffForm(request.POST, instance=staff_user)
#         profile_form = InlineStaffProfileForm(request.POST, instance=staff_profile)
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             return redirect('manage_staff')
#     else:
#         user_form = InlineStaffForm(instance=staff_user)
#         profile_form = InlineStaffProfileForm(instance=staff_profile)
    
#     context = {
#         'user_form': user_form,
#         'profile_form': profile_form,
#         'staff_user': staff_user
#     }
#     return render(request, 'hod_template/edit_staff.html', context)


@login_required
def edit_staff(request, staff_id):
    if request.user.user_type != 2:  # Check if the user is an HOD
        return HttpResponseForbidden("You are not authorized to view this page.")
    
    hod = get_object_or_404(HOD, admin=request.user)
    staff_user = get_object_or_404(CustomUser, id=staff_id)
    staff_profile = get_object_or_404(Staff, admin=staff_user)

    if staff_profile.department != hod.department:
        return HttpResponseForbidden("You are not authorized to edit this staff member.")
    
    if request.method == 'POST':
        staff_user.email = request.POST['email']
        staff_user.first_name = request.POST['first_name']
        staff_user.last_name = request.POST['last_name']
        staff_user.username = request.POST['username']
        staff_user.address = request.POST['address']
        staff_profile.department_id = request.POST['department']
        staff_profile.position = request.POST['position']
        staff_profile.gender = request.POST['gender']
        
        if 'password' in request.POST and request.POST['password']:
            staff_user.set_password(request.POST['password'])
        
        staff_user.save()
        staff_profile.save()
        
        messages.success(request, 'Staff details updated successfully!')
        return redirect('manage_staff')
    
    departments = Department.objects.all()
    context = {
        'staff_user': staff_user,
        'staff': staff_profile,
        'departments': departments,
    }
    return render(request, 'hod_template/edit_staff_template.html', context)



# @login_required
# def take_attendance(request):
#     if request.method == 'POST':
#         form = AttendanceForm(request.POST)
#         if form.is_valid():
#             hod = HOD.objects.get(admin=request.user)
#             attendance = form.save(commit=False)
#             attendance.staff = hod
#             attendance.save()
#             messages.success(request, 'Attendance has been successfully recorded.')
#             return redirect('take_attendance')
#         else:
#             messages.error(request, 'Please correct the error below.')
#     else:
#         form = AttendanceForm()
#     return render(request, 'hod/take_attendance.html', {'form': form})


# @login_required
# def hod_take_attendance(request):
#     if request.method == 'POST':
#         attendance_date = request.POST.get('attendance_date')
#         clock_in = request.POST.get('clock_in')
#         clock_out = request.POST.get('clock_out')

#         if attendance_date and clock_in and clock_out:
#             try:
#                 hod = HOD.objects.get(admin=request.user)
#                 attendance = Attendance(
#                     hod=hod,
#                     attendance_date=parse_date(attendance_date),
#                     clock_in=parse_time(clock_in),
#                     clock_out=parse_time(clock_out),
#                 )
#                 attendance.save()
#                 messages.success(request, 'Attendance has been successfully recorded.')
#                 return redirect('hod_take_attendance')
#             except Exception as e:
#                 messages.error(request, f'Error saving attendance: {e}')
#         else:
#             messages.error(request, 'All fields are required.')

#     return render(request, 'hod_template/hod_take_attendance.html')


# @login_required
# def hod_take_attendance(request):
#     hod = HOD.objects.get(admin=request.user)
#     if request.method == 'POST':
#         action = request.POST.get('action')
#         attendance_date = request.POST.get('attendance_date')

#         try:
#             attendance, created = Attendance.objects.get_or_create(
#                 hod=hod,
#                 attendance_date=parse_date(attendance_date)
#             )

#             if action == 'clock_in':
#                 clock_in = request.POST.get('clock_in')
#                 attendance.clock_in = parse_time(clock_in)
#                 messages.success(request, 'Clock-in time recorded successfully.')

#             elif action == 'clock_out':
#                 clock_out = request.POST.get('clock_out')
#                 attendance.clock_out = parse_time(clock_out)
#                 messages.success(request, 'Clock-out time recorded successfully.')

#             attendance.save()
#             return redirect('hod_take_attendance')

#         except Exception as e:
#             messages.error(request, f'Error saving attendance: {e}')
        
#     return render(request, 'hod_template/hod_take_attendance.html')
@login_required
def hod_take_attendance(request):
    hod = HOD.objects.get(admin=request.user)
    if request.method == 'POST':
        action = request.POST.get('action')
        attendance_date = request.POST.get('attendance_date')

        try:
            attendance, created = Attendance.objects.get_or_create(
                hod=hod,
                attendance_date=parse_date(attendance_date)
            )

            if action == 'clock_in':
                clock_in = request.POST.get('clock_in')
                attendance.clock_in = parse_time(clock_in)
                messages.success(request, 'Clock-in time recorded successfully.')

            elif action == 'clock_out':
                clock_out = request.POST.get('clock_out')
                attendance.clock_out = parse_time(clock_out)
                messages.success(request, 'Clock-out time recorded successfully.')

            attendance.save()
            return redirect('hod_attendance_records')

        except Exception as e:
            messages.error(request, f'Error saving attendance: {e}')
        
    return render(request, 'hod_template/hod_take_attendance.html')


@login_required
def hod_attendance_records(request):
    hod = HOD.objects.get(admin=request.user)
    attendances = Attendance.objects.filter(hod=hod).order_by('-attendance_date')

    context = {
        'attendances': attendances
    }
    return render(request, 'hod_template/hod_attendance_records.html', context)


# @login_required
# def hod_view_staff_attendance(request):
#     if request.user.user_type != 2:  # Ensure the user is an HOD
#         return HttpResponseForbidden("You are not authorized to view this page.")

#     hod = HOD.objects.get(admin=request.user)
#     attendance_records = Attendance.objects.filter(staff__department=hod.department)

#     context = {
#         'attendance_records': attendance_records,
#     }
#     return render(request, 'hod_template/hod_view_staff_attendance.html', context)


def hod_all_notification(request):
    hod = HOD.objects.get(admin=request.user.id)
    notifications = NotificationHOD.objects.filter(hod_id=hod.id)
    return render(
        request,
        "hod_template/all_notification.html",
        {"notifications": notifications},
    )
# def staff_all_notification(request):
#     staff = Staff.objects.get(admin=request.user.id)
#     notifications = NotificationStaff.objects.filter(staff_id=staff.id)
#     return render(
#         request,
#         "staff_template/all_notification.html",
#         {"notifications": notifications},
#     )

def hod_apply_leave(request):
    hod_obj = HOD.objects.get(admin=request.user.id)

    if request.method == "POST":
        leave_date = request.POST.get("leave_date")
        leave_msg = request.POST.get("leave_msg")

        try:
            leave_report = LeaveReportHOD(hod_id=hod_obj, leave_date=leave_date, leave_message=leave_msg, leave_status=0)
            leave_report.save()
            messages.success(request, "Successfully Applied for Leave")
        except Exception as e:
            messages.error(request, f"Failed To Apply for Leave: {str(e)}")
        
        return redirect('hod_apply_leave')
    
    leave_data = LeaveReportHOD.objects.filter(hod_id=hod_obj)
    return render(request, "hod_template/hod_apply_leave.html", {"leave_data": leave_data})


def hod_feedback(request):
    hod_obj = HOD.objects.get(admin=request.user.id)

    if request.method == "POST":
        feedback_msg = request.POST.get("feedback_msg")

        try:
            feedback = FeedBackHOD(hod_id=hod_obj, feedback=feedback_msg, feedback_reply="")
            feedback.save()
            messages.success(request, "Successfully Sent Feedback")
        except Exception as e:
            messages.error(request, f"Failed To Send Feedback: {str(e)}")
        
        return redirect('hod_feedback')
    
    feedback_data = FeedBackHOD.objects.filter(hod_id=hod_obj)
    return render(request, "hod_template/hod_feedback.html", {"feedback_data": feedback_data})


@csrf_exempt
def hod_fcmtoken_save(request):
    token = request.POST.get("token")
    try:
        hod = HOD.objects.get(admin=request.user.id)
        hod.fcm_token = token
        hod.save()
        return HttpResponse("True")
    except Exception:
        return HttpResponse("False")