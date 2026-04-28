from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

def calculate_similarity(resume_text, jd_text):
    tfidf = TfidfVectorizer(stop_words='english')
    vectors = tfidf.fit_transform([resume_text, jd_text])
    
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])
    
    return round(similarity[0][0] * 100, 2)

def get_missing_skills(resume, jd):
    resume_words = set(re.findall(r'\b\w+\b', resume.lower()))
    jd_words = set(re.findall(r'\b\w+\b', jd.lower()))
    
    missing = jd_words - resume_words

    stop_words = {"and", "or", "the", "with", "a", "an", "to", "of", "in"}
    filtered = [word for word in missing if word not in stop_words]

    return filtered[:10]