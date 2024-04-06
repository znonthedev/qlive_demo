from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.core.exceptions import ValidationError
# Create your models here.


class Subject(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.name


# @receiver(pre_delete, sender=Subject)
# def protect_subject_delete(sender, instance, **kwargs):
#     # Check if any teachers are associated with the subject
#     if instance.teachers.exists():
#         raise ValidationError("Cannot delete the subject as it is associated with teachers.")
    

class Grade(models.Model):
    name = models.CharField(max_length=255,unique=False)

    def __str__(self):
        return self.name
    
# @receiver(pre_delete, sender=Grade)
# def protect_grade_delete(sender, instance, **kwargs):
#     # Check if any remunerations are associated with the grade
#     if instance.grade_remunerations.exists():
#         raise ValidationError("Cannot delete the grade as it is associated with teacher")
    
class Remuneration(models.Model):
    teacher = models.ForeignKey('Teachers', on_delete=models.CASCADE, related_name='remunerations')
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='grade_remunerations')
    min_remuneration = models.DecimalField(max_digits=10, decimal_places=2)
    max_remuneration = models.DecimalField(max_digits=10, decimal_places=2)

class Teachers(models.Model):

    english_fluency_choices = [
        ('100%', 5),
        ('90%', 4.5),
        ('80%', 4),
        ('Below 80%', 3),
    ]

    interview_rating_choices = [
        ('100%', 5),
        ('90%', 4.5),
        ('80%', 4),
        ('Below 80%', 3),
    ]

    teacher_name = models.CharField(max_length=255, null=False, blank=False)
    roll_no = models.CharField(max_length=25, null=True, blank=True)
    subject = models.ManyToManyField(
        Subject, related_name="teachers_subject",blank=True
    )
    # grade = models.ManyToManyField(
    #     Grade, related_name="teacher_grades",blank=True
    # )
    whatsapp_no = models.CharField(max_length=25, null=True, blank=True)
    contact_no = models.CharField(max_length=25, null=True, blank=True)
    email = models.EmailField(max_length=255,null=False,blank=False)
    experience = models.FloatField(default=0, null=True, blank=True)
    english_fluency = models.CharField(max_length=15, choices=english_fluency_choices,null=True,blank=True)
    interview_rating = models.CharField(max_length=15, choices=interview_rating_choices,null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True)
    video_link = models.URLField(null=True, blank=True)
    bank_acc_holder_name = models.CharField(max_length=255, null=True, blank=True)
    bank_name = models.CharField(max_length=255, null=True, blank=True)
    account_no = models.CharField(max_length=50, null=True, blank=True)
    branch = models.CharField(max_length=255, null=True, blank=True)
    ifsc_code = models.CharField(max_length=255, null=True, blank=True)
    google_pay = models.CharField(max_length=25, null=True, blank=True)
    phone_pay = models.CharField(max_length=25, null=True, blank=True)
    success_demo = models.IntegerField(default=0)
    failed_demo = models.IntegerField(default=0)
    teacher_change = models.IntegerField(default=0)
    about = models.TextField(null=True, blank=True)
    remark = models.TextField(null=True, blank=True)
    qualification = models.CharField(max_length=255, null=True, blank=True)
    black_list = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

# @receiver(pre_delete, sender=Subject)
# def protect_subject_delete(sender, instance, **kwargs):
#     # Check if any teachers are associated with the subject
#     if Teachers.objects.filter(subject=instance).exists():
#         raise ValidationError("Cannot delete the subject as it is associated with teachers.")