from django import forms
from .models import Feedback,Course,Instructor,Student

class FeedBackForm(forms.ModelForm):
    class Meta:
        model=Feedback
        fields=['course','instructor','out_of_syllabus','time_sufficiency','nature','comments']
        widgets={
            'comments':forms.Textarea(attrs={'rows':3}),
        }
        