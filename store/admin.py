from django.contrib import admin
from .models import Subject,Teachers,Grade,Remuneration

# Register your models here.


class SubjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
admin.site.register(Subject, SubjectAdmin)

class GradeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
admin.site.register(Grade, GradeAdmin)

class RemunerationAdmin(admin.ModelAdmin):
    list_display = ("id", "teacher","grade","min_remuneration","max_remuneration")
admin.site.register(Remuneration, RemunerationAdmin)


class TeachersAdmin(admin.ModelAdmin):
    list_display = [
        "id", 
        "teacher_name",
        "roll_no",
        "whatsapp_no",
        "contact_no",
        "email",
        "experience",
        "date",
        "video_link",
        "bank_acc_holder_name",
        "bank_name",
        "branch",
        "account_no",
        "ifsc_code",
        "google_pay",
        "phone_pay",
        "about",
        "remark",
        "qualification",
        "english_fluency",
        "interview_rating",
        
        ]
admin.site.register(Teachers, TeachersAdmin)

