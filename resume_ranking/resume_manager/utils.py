# resumes/utils.py
from .models import JobDescription, Resume, RankingResult
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import textract
from pdfminer.high_level import extract_text
from transformers import BertTokenizer, BertModel
import torch
import os
from django.conf import settings
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def rank_resumes(session_id,model_choice):
    jd = JobDescription.objects.get(session_id=session_id)
    resumes = Resume.objects.filter(session_id=session_id)

    # ranked_resumes = []
     # Process the job description and resumes based on the model choice
    if model_choice == 'tfidf':
        # Use TF/IDF model for ranking
        rank_using_tfidf(jd, resumes)
    elif model_choice == 'doc2vec':
        # Use Word2Vec model for ranking
        rank_using_doc2vec(jd, resumes)
    elif model_choice == 'bert':
        # Use BERT model for ranking
        rank_using_bert(jd, resumes)
    else:
        raise ValueError("Invalid model choice")
    

def extract_text_from_file(file_path):
    print(f"extracting text from {file_path}")
    print(f"extracting text from {type(file_path)}")

    try:
        text = extract_text(file_path)  # Pass the file path directly
        print(f"extracting text from {file_path} successfull text is {text[-40:]}")
        
    except Exception as e:
        print(f"Exception has been captured: {e}")
        text = ""
    return text


def rank_using_tfidf(jd, resumes):
    jd_text = jd.description
    resume_texts = []
    resume_files = []

    for resume in resumes:
        file_name=resume.file.name
        file_name= f'' + file_name[1:]
        file_path = os.path.join(settings.MEDIA_ROOT, resume.file.name)
        
        text = extract_text_from_file(file_path)
        resume_texts.append(text)
        resume_files.append(resume.file.name)

    documents = [jd_text] + resume_texts
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)

    jd_vector = tfidf_matrix[0]
    resume_vectors = tfidf_matrix[1:]

    scores = cosine_similarity(jd_vector, resume_vectors).flatten()

    ranked_resumes = sorted(zip(scores, resume_files), reverse=True)

    # Save the results in the database
    for score, file_name in ranked_resumes:
        resume = resumes.get(file=file_name)
        RankingResult.objects.create(session_id=jd.session_id, resume=resume, score=score)
    print(f"""
Ranked Resumes scores are:
          
          {ranked_resumes}""")
    return ranked_resumes

# def rank_using_doc2vec(jd, resumes):

def rank_using_doc2vec(jd, resumes):
    jd_text = jd.description
    resume_texts = []
    resume_files = []

    for resume in resumes:
        file_path = os.path.join(settings.MEDIA_ROOT, resume.file.name)
        text = extract_text_from_file(file_path)
        resume_texts.append(text)
        resume_files.append(resume.file.name)

    # Prepare the documents for Doc2Vec
    documents = [TaggedDocument(words=jd_text.split(), tags=["JOB_DESCRIPTION"])]
    for i, text in enumerate(resume_texts):
        documents.append(TaggedDocument(words=text.split(), tags=[f"RESUME_{i}"]))

    # Create and train the Doc2Vec model
    model = Doc2Vec(documents, vector_size=100, window=2, min_count=1, workers=4, epochs=100)

    # Infer vectors
    jd_vector = model.infer_vector(jd_text.split())
    resume_vectors = [model.infer_vector(text.split()) for text in resume_texts]

    # Calculate similarities
    scores = cosine_similarity([jd_vector], resume_vectors).flatten()

    ranked_resumes = sorted(zip(scores, resume_files), reverse=True)

    # Save the results in the database
    for score, file_name in ranked_resumes:
        resume = resumes.get(file=file_name)
        RankingResult.objects.create(session_id=jd.session_id, resume=resume, score=score)
    print(f"Ranked Resumes scores are: {ranked_resumes}")
    return ranked_resumes



def rank_using_bert(jd, resumes):
    jd_text = jd.description
    resume_texts = []
    resume_files = []

    for resume in resumes:
        file_path = os.path.join(settings.MEDIA_ROOT, resume.file.name)
        text = extract_text_from_file(file_path)
        resume_texts.append(text)
        resume_files.append(resume.file.name)

    # Load pre-trained BERT model and tokenizer
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')

    # Encode the job description
    jd_encoding = tokenizer(jd_text, return_tensors='pt', padding=True, truncation=True, max_length=512)
    jd_output = model(**jd_encoding)
    jd_vector = jd_output.last_hidden_state.mean(dim=1).detach().numpy()

    resume_vectors = []
    for text in resume_texts:
        resume_encoding = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512)
        resume_output = model(**resume_encoding)
        resume_vector = resume_output.last_hidden_state.mean(dim=1).detach().numpy()
        resume_vectors.append(resume_vector)

    # Convert resume_vectors to 2D array
    resume_vectors = np.vstack(resume_vectors)

    # Calculate similarities
    scores = cosine_similarity(jd_vector, resume_vectors).flatten()

    ranked_resumes = sorted(zip(scores, resume_files), reverse=True)

    # Save the results in the database
    for score, file_name in ranked_resumes:
        resume = resumes.get(file=file_name)
        RankingResult.objects.create(session_id=jd.session_id, resume=resume, score=score)
    print(f"Ranked Resumes scores are: {ranked_resumes}")
    return ranked_resumes


def calculate_similarity(jd_text, resume_path):
    with open(resume_path, 'r') as f:
        resume_text = f.read()
    score = len(set(jd_text.split()) & set(resume_text.split()))
    return score
