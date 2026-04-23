from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from templates.resume_utils import extract_text_from_pdf, clean_text, get_similarity, extract_skills

app = Flask(__name__)

# Secret key (required for session)
app.secret_key = "supersecretkey"

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)


# DATABASE MODEL
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))

# Create DB
with app.app_context():
    db.create_all()


# ROUTES
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/login-page')
def login_page():
    return render_template("login_page.html")

@app.route('/signup-page')
def signup_page():
    return render_template("signup_page.html")

# SIGNUP

@app.route('/signup', methods=['POST'])
def signup():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    # Hash password
    hashed_password = generate_password_hash(password)

    # Save user
    new_user = User(name=name, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('login_page'))


# LOGIN

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        session['user'] = user.name
        return redirect(url_for('home'))
    else:
        return "Invalid email or password"


# LOGOUT

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))


# PROTECTED PAGE

@app.route('/analyze-page')
def analyze_page():
    if 'user' not in session:
        return redirect(url_for('login_page'))
    return render_template("analyze.html")

# -------------------------
# ANALYZE
# -------------------------
@app.route('/analyze', methods=['POST'])
def analyze():
    if 'user' not in session:
        return redirect(url_for('login_page'))

    file = request.files['resume']
    jd = request.form['job_desc']

    resume_text = extract_text_from_pdf(file)

    resume_clean = clean_text(resume_text)
    jd_clean = clean_text(jd)

    score = get_similarity(resume_clean, jd_clean)

    skills_list = ["python", "java", "c", "c++", "sql", "machine learning",
                   "html", "css", "javascript", "node", "artificial intelligence"]

    matched = extract_skills(resume_clean, skills_list)
    missing = list(set(skills_list) - set(matched))

    return render_template("result.html",
                           score=round(score * 10, 2),
                           matched=matched,
                           missing=missing)

if __name__ == "__main__":
    app.run(debug=True)