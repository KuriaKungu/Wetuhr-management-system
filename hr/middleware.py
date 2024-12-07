from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

class LoginCheckMiddleWare(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        user = request.user

        # Check if the request is for a static file or media file
        if modulename.startswith('django.contrib.staticfiles') or request.path.startswith(settings.MEDIA_URL):
            return None

        if user.is_authenticated:
            if user.user_type == "1":
                if modulename == "hr.adminviews":
                    pass
                elif modulename == "hr.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("admin_home"))
            elif user.user_type == "2":
                if modulename == "hr.hodviews":
                    pass
                elif modulename == "hr.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("hod_home_template"))
            elif user.user_type == "3":
                if modulename == "hr.staffviews":
                    pass
                elif modulename == "hr.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("staff_home_template"))
            else:
                return HttpResponseRedirect(reverse("show_login"))

        else:
            if request.path == reverse("show_login") or request.path == reverse("do_login") or modulename == "django.contrib.auth.views":
                pass
            else:
                return HttpResponseRedirect(reverse("show_login"))
