import PyPDF2
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Extract text from PDF
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""

    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content

    return text.strip()

# Clean text
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z ]', ' ', text)
    return " ".join(text.split())  # remove extra spaces

# Calculate similarity
def get_similarity(resume, jd):
    tfidf = TfidfVectorizer(stop_words='english')
    vectors = tfidf.fit_transform([resume, jd])
    score = cosine_similarity(vectors[0:1], vectors[1:2])
    return round(score[0][0] * 100, 2)  # return %

# Extract skills
def extract_skills(text, skills_list):
    text = text.lower()
    found = [skill for skill in skills_list if skill.lower() in text]
    return list(set(found))