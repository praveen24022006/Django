from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Department(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name
class Course(models.Model):
    code=models.CharField(max_length=100,unique=True)
    name=models.CharField(max_length=200)
    department=models.ForeignKey(Department,on_delete=models.SET_NULL,null=True,blank=True)
    def __str__(self):
        return  f"{self.code}-{self.name}"
class Instructor(models.Model):
    user=models.OneToOneField(User,on_delete=models.SET_NULL,null=True,blank=True)
    name=models.CharField(max_length=150)
    courses=models.ManyToManyField(Course,blank=True)
    def __str__(self):
        return self.name
class Student(models.Model):
    user=models.OneToOneField(User,on_delete=models.SET_NULL,null=True,blank=True)
    roll_no=models.CharField(max_length=100,unique=True)
    name=models.CharField(max_length=150)
    department=models.ForeignKey(Department,on_delete=models.SET_NULL,null=True,blank=True)
    def __str__(self):
        return f"{self.roll_no}-{self.name}"

STANDARDS=[('Good','Good'),('Medium','Medium'),('Low','Low'),]
YESNO=[('Yes','Yes'),('No','No'),]
NATURE=[('Tough','Tough'),('Normal','Normal'),('Easy','Easy'),]
TIME_SUFF = [
    ('Sufficient', 'Sufficient'),
    ('Insufficient', 'Insufficient'),
]

class Feedback(models.Model):
    Student=models.ForeignKey(Student,on_delete=models.SET_NULL,null=True,blank=True)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    instructor=models.ForeignKey(Instructor,on_delete=models.SET_NULL,null=True,blank=True)
    out_of_syllabus=models.CharField(max_length=3,choices=YESNO,default='No')
    standard=models.CharField(max_length=10,choices=STANDARDS,default="No")
    time_sufficiency=models.CharField(max_length=12,choices=TIME_SUFF,default="Sufficient")
    nature=models.CharField(max_length=10,choices=NATURE,default="Normal")
    comments=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Feedback {self.id}-{self.course.code}"
