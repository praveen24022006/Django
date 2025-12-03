from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
# Create your views here.
from django.urls import reverse
from django.db import models

from django.contrib.auth.decorators import login_required
from .models import Feedback,Course,Instructor
from .forms import FeedBackForm
import csv

def home(request):
    form=FeedBackForm(request.POST)
    if request.method=="POST":
        fb=form.save(commit=False)
        if request.user.is_authenticated:
            try:
                fb.student=request.user.student
            except:
                pass
        fb.save()
        if request.headers.get('x-requested-with')=="XMLHttpRequest":
            return JsonResponse({'ok':True})
        return redirect(reverse('Feedback:dashboard'))
    total=Feedback.objects.count()
    by_standard=Feedback.objects.values('standard').order_by().annotate(count=models.Count('id'))
    return render(request,'Feedback/dashboard.html',{'form':form,'total':total})

def api_feedback_stats(request):
    from django.db.models import Count
    by_out_of_syllabus = Feedback.objects.values('out_of_syllabus').annotate(count=Count('id'))
    by_time=Feedback.objects.values('time_sufficiency').annotate(count=Count('id'))
    by_nature=Feedback.objects.values('nature').annotate(count=Count('id'))
    return JsonResponse({
        'by_out_of_syllabus': list(by_out_of_syllabus),
        'by_time':list(by_time),
        'by_nature':list(by_nature),
        'total':Feedback.objects.count()
    })


def export_csv(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect(f'/admin/login/?next={request.path}')
    qs=Feedback.objects.select_related('course','instructor','Student').all().order_by('-created_at')
    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="feedback_export.csv"'
    writer = csv.writer(response)
    writer.writerow(['id','course_code','course_name','instructor','student_roll','standard','time_sufficiency','out_of_syllabus','nature','comments','created_at'])
    for f in qs:
        student_obj = getattr(f, 'student', None) or getattr(f, 'Student', None)
        writer.writerow([
            f.id,
            f.course.code if f.course else '',
            f.course.name if f.course else '',
            f.instructor.name if f.instructor else '',
            f.Student.roll_no if f.Student else '',
            f.standard,
            f.time_sufficiency,
            f.out_of_syllabus,
            f.nature,
            f.comments,
            f.created_at.isoformat()
        ])
    return response