# resumes/views.py
from django.shortcuts import render, redirect
from .forms import JobDescriptionForm, ResumeForm, SimpleFileUploadForm
from .models import JobDescription, Resume, RankingResult
import uuid
import os
import os
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from .forms import SimpleFileUploadForm

def simple_file_upload(request):
    if request.method == 'POST':
        form = SimpleFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            with open(os.path.join(settings.MEDIA_ROOT, file.name), 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            return HttpResponse('File uploaded successfully')
    else:
        form = SimpleFileUploadForm()
    return render(request, 'resume_manager/simple_upload.html', {'form': form})

def upload_resume(request):
    if request.method == 'POST':
        print("post method detected")
        jd_form = JobDescriptionForm(request.POST)
        resume_form = ResumeForm(request.POST, request.FILES)
        if not jd_form.is_valid():
            print("Job Description Form Errors: ", jd_form.errors)
        else:
            print("Job Description : ", jd_form.__dict__)

# Check if Resume form is valid
        if not resume_form.is_valid():
            print("Resume Form Errors: ", resume_form.errors)
        if jd_form.is_valid() and resume_form.is_valid():
            jd = jd_form.save(commit=False)
            session_id = uuid.uuid4()
            jd.session_id = session_id
            # print(jd.)
            jd.save()
            # print(f"Files: {files}")  # Debugging print statement
            
            files = request.FILES.getlist('files')
            for file in files:
                print(f"Processing file: {file.name}")  # Debugging print statement
                Resume.objects.create(session_id=session_id, file=file)
            
            # Process and rank resumes in the background
            # rank_resumes(session_id)
            
            return redirect('rank_results', session_id=session_id)
    else:
        jd_form = JobDescriptionForm()
        resume_form = ResumeForm()
    return render(request, 'resume_manager/upload_resumes.html', {'jd_form': jd_form, 'resume_form': resume_form})

def rank_results(request, session_id):
    results = RankingResult.objects.filter(session_id=session_id).order_by('-score')
    return render(request, 'resume_manager/rank_results.html', {'results': results})
