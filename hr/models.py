from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import ValidationError

# Department model
class Department(models.Model):
    department_name = models.CharField(max_length=255)

    def __str__(self):
        return self.department_name

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, username, password, **extra_fields)

# Custom User model extending AbstractUser
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'Admin'),
        (2, 'HOD'),
        (3, 'Staff')
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=1)
    email = models.EmailField(unique=True)
    address = models.TextField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

class HOD(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='hod_profile')
    address = models.TextField()
    gender = models.CharField(max_length=255, default='Male')
    profile_pic = models.ImageField (
        upload_to ='hod_profile_pics/',
        blank = True,
        null = True,
        help_text = "Upload a profile picture"
    )
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    fcm_token = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.admin.first_name} {self.admin.last_name} - {self.department.department_name}"


class Staff(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='staff_profile')
    address = models.TextField()
    gender = models.CharField(max_length=255, default='Male')
    profile_pic = models.ImageField(
        upload_to='staff_profile_pics/',
        blank=True,
        null=True,
        help_text="Upload a profile picture"
    )
    position = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    fcm_token = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.admin.username

class Admin(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='admin_profile')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.admin.username

# class Attendance(models.Model):
#     id = models.AutoField(primary_key=True)
#     staff = models.ForeignKey(Staff, on_delete=models.DO_NOTHING, null=True)
#     hod = models.ForeignKey(HOD, on_delete=models.DO_NOTHING, null=True, blank=True)  # To track HOD attendance
#     attendance_date = models.DateField()
#     clock_in = models.TimeField(null=True, blank=True)
#     clock_out = models.TimeField(null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     status = models.BooleanField(default=False)

#     def __str__(self):
#         return f"{self.staff.admin.username if self.staff else self.hod.admin.username} - {self.attendance_date}"


class Attendance(models.Model):
    id = models.AutoField(primary_key=True)
    staff = models.ForeignKey(Staff, on_delete=models.DO_NOTHING, null=True)
    hod = models.ForeignKey(HOD, on_delete=models.DO_NOTHING, null=True, blank=True)  # To track HOD attendance
    attendance_date = models.DateField()
    clock_in = models.TimeField(null=True, blank=True)
    clock_out = models.TimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.staff.admin.username if self.staff else self.hod.admin.username} - {self.attendance_date}"

class LeaveRequest(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    leave_date = models.DateField()
    leave_message = models.TextField()
    status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.leave_date}"

class LeaveReportHOD(models.Model):
    id = models.AutoField(primary_key=True)
    hod_id = models.ForeignKey(HOD, on_delete=models.CASCADE)
    leave_date = models.DateField()
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.hod_id.admin.username} - {self.leave_date}"

class LeaveReportStaff(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    leave_date = models.DateField()
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.staff_id.admin.username} - {self.leave_date}"

class FeedBackHOD(models.Model):
    id = models.AutoField(primary_key=True)
    hod_id = models.ForeignKey(HOD, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.hod_id.admin.username} - {self.created_at}"

class FeedBackStaff(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.staff_id.admin.username} - {self.created_at}"

class NotificationHOD(models.Model):
    id = models.AutoField(primary_key=True)
    hod_id = models.ForeignKey(HOD, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.hod_id.admin.username} - {self.created_at}"

class NotificationStaff(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.staff_id.admin.username} - {self.created_at}"

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            Admin.objects.create(admin=instance)
        elif instance.user_type == 2:
            pass
        elif instance.user_type == 3:
            pass

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1 and hasattr(instance, 'admin_profile'):
        instance.admin_profile.save()
    elif instance.user_type == 2 and hasattr(instance, 'hod_profile'):
        instance.hod_profile.save()
    elif instance.user_type == 3 and hasattr(instance, 'staff_profile'):
        instance.staff_profile.save()
