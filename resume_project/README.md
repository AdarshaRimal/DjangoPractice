# AI Resume & Cover Letter Generator

AI tool to extract resume skills and create custom cover letters.

## Features
- Upload PDF/DOCX resumes
- Extract skills with AI
- Generate cover letters from job descriptions
- Download as PDF

## Tech Used
- Django
- Hugging Face API
- ReportLab (PDF)
- Bootstrap

## Setup
```bash
# Clone repo
git clone https://github.com/AdarshaRimal/DJANGOPRACTICE
cd DJANGOPRACTICE/resume_project

# Create virtual environment
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# Install packages
pip install -r requirements.txt

# Create .env file
echo "HUGGING_FACE_TOKEN=your_token" > .env
echo "SECRET_KEY=your_django_key" >> .env

# Run server
python manage.py migrate
python manage.py runserver

## How To Use
1. Sign up at `/signup`
2. Upload resume
3. Enter job description
4. Edit & download cover letter

## Requirements
- Python 3.8+
- Hugging Face API token