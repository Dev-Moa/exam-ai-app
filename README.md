# Exam AI: Backend

AI-powered exam review API. Students submit their exam results, and the system produces a structured review: final score, incorrect answers, and the correct versions. So learners see exactly where they lost marks and why.

## Background

Built as my **final-year graduation project** for my B.Sc. in Computer Applications at Jamhuriya University of Science and Technology (graduated December 2024).

## How it works

1. An AI model analyzes the submitted exam result
2. The response is parsed into structured data (student, book/subject, score, per-question breakdown)
3. Results are stored and served to the frontend dashboard

## Tech stack

- **Django 4.2** + **Django REST Framework**
- JWT authentication
- **PostgreSQL** · **Gunicorn** · **Railway**

## Models

- `StudentReview` — one review per submission (student, book, final score, incorrect-answer count, detailed breakdown)
- `QuestionDetail` — per-question result with the correct version

## Frontend

See [exam-ai-ui](https://github.com/Dev-Moa/exam-ai-ui) — Vue 3 + Tailwind.

## Local setup

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
