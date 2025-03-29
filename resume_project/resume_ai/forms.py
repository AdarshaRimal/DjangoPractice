from django import forms
from .models import Resume, CoverLetter

class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['file']

class JobDescriptionForm(forms.Form):
    job_description = forms.CharField(widget=forms.Textarea)

class CoverLetterForm(forms.ModelForm):
    class Meta:
        model = CoverLetter
        fields = ['edited_text']