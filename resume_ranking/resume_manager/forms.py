# resumes/forms.py
from django import forms
from .models import JobDescription

class JobDescriptionForm(forms.ModelForm):
    MODEL_CHOICES = [
        ('tfidf', 'TF/IDF'),
        ('doc2vec', 'Doc2Vec'),
        ('bert', 'BERT'),
    ]
    
    model_choice = forms.ChoiceField(
        choices=MODEL_CHOICES, 
        label="Select Ranking Model",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = JobDescription
        fields = ['description', 'model_choice']
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 5, 
                'placeholder': 'Enter job description'
            }),
        }

# forms.py
class SimpleFileUploadForm(forms.Form):
    file = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control-file'})
    )

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput(attrs={'class': 'form-control-file'}))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class ResumeForm(forms.Form):
    files = MultipleFileField()
