# resume_ai/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Resume, CoverLetter
from .forms import ResumeUploadForm, JobDescriptionForm, CoverLetterForm
from .utils import extract_text
from .llm_utils import analyze_resume_skills, generate_cover_letter  # UPDATED IMPORT
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from io import BytesIO
from .models import CoverLetter

@login_required
def upload_resume(request):
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()
            
            # Extract text and analyze
            text = extract_text(resume.file.path)
            resume.extracted_text = text
            resume.skills = analyze_resume_skills(text)  # UPDATED FUNCTION NAME
            resume.save()
            return redirect('generate_cover', resume_id=resume.id)
    else:
        form = ResumeUploadForm()
    return render(request, 'resume_ai/upload_resume.html', {'form': form})

@login_required
def generate_cover(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    if request.method == 'POST':
        form = JobDescriptionForm(request.POST)
        if form.is_valid():
            jd = form.cleaned_data['job_description']
            cover_text = generate_cover_letter(resume.skills, jd)
            cover_letter = CoverLetter.objects.create(
                resume=resume,
                job_description=jd,
                generated_text=cover_text,
                edited_text=cover_text
            )
            return redirect('edit_cover', cover_id=cover_letter.id)
    else:
        form = JobDescriptionForm()
    return render(request, 'resume_ai/generate_cover.html', {'form': form, 'resume': resume})

@login_required
def edit_cover(request, cover_id):
    cover = get_object_or_404(CoverLetter, id=cover_id, resume__user=request.user)
    if request.method == 'POST':
        form = CoverLetterForm(request.POST, instance=cover)
        if form.is_valid():
            form.save()
            return redirect('download', cover_id=cover.id)
    else:
        form = CoverLetterForm(instance=cover)
    return render(request, 'resume_ai/edit_cover.html', {'form': form, 'cover': cover})

@login_required
def dashboard(request):
    resumes = Resume.objects.filter(user=request.user)
    return render(request, 'resume_ai/dashboard.html', {'resumes': resumes})

class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = 'resume_ai/signup.html'
    success_url = reverse_lazy('login')

@login_required
def download_cover(request, cover_id):
    cover = get_object_or_404(CoverLetter, id=cover_id, resume__user=request.user)
    
    # Create PDF
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Set font and position
    p.setFont("Helvetica", 12)
    text = p.beginText(1 * inch, 10 * inch)
    text.textLines(cover.edited_text)
    
    # Add content
    p.drawText(text)
    p.showPage()
    p.save()
    
    # Prepare response
    pdf = buffer.getvalue()
    buffer.close()
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=cover_letter_{cover.id}.pdf'
    response.write(pdf)
    return response