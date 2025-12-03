from django.contrib import admin
from .models import Department,Course,Instructor,Student,Feedback
# Register your models here.
class DepartmentAdmin(admin.ModelAdmin):
    list_display=('name',)
class CoursreAdmin(admin.ModelAdmin):
    list_display=('code','name','department')
    search_fields=('code','name')
class InstructorAdmin(admin.ModelAdmin):
    list_display=('name',)
class StudentAdmin(admin.ModelAdmin):
    list_display=('roll_no.','name','department')
class FeedbackAdmin(admin.ModelAdmin):
    list_display=('id','course','instructor','standard','time_sufficiency','created_at')
    list_filter=('standard','time_sufficiency','created_at','course')
    search_fields=('course__code','course__name','instructor__name','student__roll_no')
# feedback/admin.py
from django.contrib import admin
from .models import Department, Course, Instructor, Student, Feedback

admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Instructor)
admin.site.register(Student)
admin.site.register(Feedback)

