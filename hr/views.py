from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# This is the decorator to ensure the user is authenticated before proceeding
def check_authenticated_user(view_func):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('admin_home')  # Redirect authenticated users to their respective page
        return view_func(request, *args, **kwargs)
    return wrap

# This decorator ensures the user is an admin and not a staff or HOD
def admin_only(view_func):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type != 1:
            # Redirect to a page not allowed for this user type (e.g., 403 error or home page)
            return HttpResponseRedirect(reverse('not_allowed'))  # Change 'not_allowed' to your error page
        return view_func(request, *args, **kwargs)
    return wrap

# Admin Home page (accessible by admins only)
@admin_only
def admin_home(request):
    return render(request, 'admin_home.html')

# HOD Home page (accessible by HOD only)
@admin_only
def hod_home(request):
    return render(request, 'hod_home.html')

# Staff Home page (accessible by staff only)
@admin_only
def staff_home(request):
    return render(request, 'staff_home.html')


def showDemoPage(request):
    return render(request, "demo.html")

# Login page view
@check_authenticated_user
def showLoginPage(request):
    return render(request, "login_page.html")


@csrf_protect
def doLogin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Try authenticating the user
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome, {email}!')

            # Check user type and redirect accordingly
            try:
                if user.user_type == 1:  # Admin
                    return HttpResponseRedirect(reverse("admin_home"))
                elif user.user_type == 2:  # HOD
                    return HttpResponseRedirect(reverse("hod_home"))
                elif user.user_type == 3:  # Staff
                    return HttpResponseRedirect(reverse("staff_home"))
                else:
                    # Default redirect if user_type is not recognized
                    return HttpResponseRedirect('/')
            except ObjectDoesNotExist:
                return HttpResponse("Profile does not exist.")
        else:
            messages.error(request, 'Invalid Login')
            return JsonResponse({'error': 'Invalid Login'}, status=401)

    elif request.method == "GET":
        return render(request, "login_page.html")
    else:
        return HttpResponse("<h2> Method Not Allowed </h2>")


def GetUserDetails(request):
    if request.user.is_authenticated:
        return HttpResponse(
            "User : "
            + request.user.email
            + " usertype : "
            + str(request.user.user_type)
        )
    else:
        return HttpResponse("Please Login First")


# Logout functionality
def logout_User(request):
    logout(request)
    return HttpResponseRedirect("/")


def showFirebaseJS(request):
    data = (
        'importScripts("https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js");'\
        'importScripts("https://www.gstatic.com/firebasejs/10.12.2/firebase-messaging.js"); ' \
        "var firebaseConfig = {" \
        '        apiKey: "AIzaSyBwqY2ru4AHb9gvcwZ-TI8xQjbUKIM9YnI",' \
        '        authDomain: "hr-management-system-6b541.firebaseapp.com",' \
        '        projectId: "hr-management-system-6b541",' \
        '        storageBucket: "hr-management-system-6b541.appspot.com",' \
        '        messagingSenderId: "140280377124",' \
        '        appId: "1:140280377124:web:97f9c2b4a17029229a4db1",' \
        '        measurementId: "G-PBDXE5E9LE"' \
        ' };' \
        'firebase.initializeApp(firebaseConfig);' \
        'const messaging=firebase.messaging();' \
        'messaging.setBackgroundMessageHandler(function (payload) {' \
        '    console.log(payload);' \
        '    const notification=JSON.parse(payload);' \
        '    const notificationOption={' \
        '        body:notification.body,' \
        '        icon:notification.icon' \
        '    };' \
        '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
        '});'
    )
    return HttpResponse(data, content_type="text/javascript")
