from django.shortcuts import render, redirect
from django.utils.dateparse import parse_date, parse_time
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
import json
from .models import FeedBackStaff, LeaveReportStaff, LeaveRequest, NotificationStaff, Staff, Attendance

@login_required
def staff_home(request):
    staff = Staff.objects.get(admin=request.user)
    total_leaves = LeaveRequest.objects.filter(user=request.user).count()
    notifications = NotificationStaff.objects.filter(staff_id=staff).count()
    feedback_count = FeedBackStaff.objects.filter(staff_id=staff).count()

    attendance_present_list_staff = Attendance.objects.filter(staff=staff, status=True).count()
    attendance_absent_list_staff = Attendance.objects.filter(staff=staff, status=False).count()

    context = {
        'total_leaves': total_leaves,
        'notifications': notifications,
        'feedback_count': feedback_count,
        'attendance_present_list_staff': attendance_present_list_staff,
        'attendance_absent_list_staff': attendance_absent_list_staff
    }
    return render(request, "staff_template/staff_home_template.html", context)

@login_required
def take_attendance(request):
    # Retrieve any messages to display to the user
    messages_list = messages.get_messages(request)
    context = {
        'messages': messages_list
    }
    return render(request, 'staff_template/staff_take_attendance.html', context)

@csrf_exempt
def get_staff(request):
    if request.method == 'POST':
        # Retrieve all staff
        staff = Staff.objects.all().values('id', 'admin__username')
        staff_list = list(staff)
        return JsonResponse(staff_list, safe=False)

# @csrf_exempt
# def save_attendance_data(request):
#     if request.method == 'POST':
#         data = json.loads(request.POST['staff_ids'])
#         attendance_date = request.POST['attendance_date']
#         clock_in = request.POST['clock_in']
#         clock_out = request.POST['clock_out']

#         for entry in data:
#             staff = Staff.objects.get(id=entry['id'])
#             attendance, created = Attendance.objects.get_or_create(
#                 staff=staff,
#                 attendance_date=attendance_date,
#                 defaults={'status': entry['status']}
#             )
#             if not created:
#                 attendance.status = entry['status']
#                 attendance.save()

#             attendance_report, created = AttendanceReport.objects.get_or_create(
#                 attendance=attendance,
#                 defaults={'status': entry['status']}
#             )
#             if not created:
#                 attendance_report.status = entry['status']
#                 attendance_report.save()

#         return JsonResponse({'status': 'OK'})
#     return JsonResponse({'status': 'FAIL'})


@login_required
def staff_take_attendance(request):
    if request.method == 'POST':
        attendance_date = request.POST.get('attendance_date')
        action = request.POST.get('action')
        clock_in = request.POST.get('clock_in')
        clock_out = request.POST.get('clock_out')

        if attendance_date and (clock_in or clock_out):
            try:
                staff = Staff.objects.get(admin=request.user)
                attendance, created = Attendance.objects.get_or_create(
                    staff=staff,
                    attendance_date=parse_date(attendance_date)
                )

                if action == 'clock_in' and clock_in:
                    attendance.clock_in = parse_time(clock_in)
                    messages.success(request, 'Clock-in time recorded successfully.')
                elif action == 'clock_out' and clock_out:
                    attendance.clock_out = parse_time(clock_out)
                    messages.success(request, 'Clock-out time recorded successfully.')

                attendance.save()
                return redirect('staff_attendance_records')
            except Exception as e:
                messages.error(request, f'Error saving attendance: {e}')
        else:
            messages.error(request, 'All fields are required.')

    return render(request, 'staff_template/staff_take_attendance.html')


@login_required
def staff_attendance_records(request):
    staff = Staff.objects.get(admin=request.user)
    attendances = Attendance.objects.filter(staff=staff).order_by('-attendance_date')

    context = {
        'attendances': attendances
    }
    return render(request, 'staff_template/staff_attendance_records.html', context)


def staff_all_notification(request):
    staff = Staff.objects.get(admin=request.user.id)
    notifications = NotificationStaff.objects.filter(staff_id=staff.id)
    return render(
        request,
        "staff_template/all_notification.html",
        {"notifications": notifications},
    )


def staff_apply_leave(request):
    staff_obj = Staff.objects.get(admin=request.user.id)

    if request.method == "POST":
        leave_date = request.POST.get("leave_date")
        leave_msg = request.POST.get("leave_msg")

        try:
            leave_report = LeaveReportStaff(staff_id=staff_obj, leave_date=leave_date, leave_message=leave_msg, leave_status=0)
            leave_report.save()
            messages.success(request, "Successfully Applied for Leave")
        except Exception as e:
            messages.error(request, f"Failed To Apply for Leave: {str(e)}")
        
        return redirect('staff_apply_leave')
    
    leave_data = LeaveReportStaff.objects.filter(staff_id=staff_obj)
    return render(request, "staff_template/staff_apply_leave.html", {"leave_data": leave_data})


def staff_feedback(request):
    staff_obj = Staff.objects.get(admin=request.user.id)

    if request.method == "POST":
        feedback_msg = request.POST.get("feedback_msg")

        try:
            feedback = FeedBackStaff(staff_id=staff_obj, feedback=feedback_msg, feedback_reply="")
            feedback.save()
            messages.success(request, "Successfully Sent Feedback")
        except Exception as e:
            messages.error(request, f"Failed To Send Feedback: {str(e)}")
        
        return redirect('staff_feedback')
    
    feedback_data = FeedBackStaff.objects.filter(staff_id=staff_obj)
    return render(request, "staff_template/staff_feedback.html", {"feedback_data": feedback_data})


@csrf_exempt
def staff_fcmtoken_save(request):
    token = request.POST.get("token")
    try:
        staff = Staff.objects.get(admin=request.user.id)
        staff.fcm_token = token
        staff.save()
        return HttpResponse("True")
    except Exception:
        return HttpResponse("False")