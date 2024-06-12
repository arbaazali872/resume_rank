# resumes/forms.py
from django import forms
from .models import JobDescription,Resume

class JobDescriptionForm(forms.ModelForm):
    MODEL_CHOICES = [
        ('tfidf', 'TF/IDF'),
        ('doc2vec', 'Doc2Vec'),
        ('bert', 'BERT'),
    ]
    
    model_choice = forms.ChoiceField(choices=MODEL_CHOICES, label="Select Ranking Model")

    class Meta:
        model = JobDescription
        fields = ['description', 'model_choice']


# forms.py
class SimpleFileUploadForm(forms.Form):
    file = forms.FileField()


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
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