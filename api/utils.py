import re
from .models import StudentReview,QuestionDetail

# extract response
def extract_details_from_string(response):
    # Extract general information
    student_name_match = re.search(r'"student_name": "([^"]+)"', response)
    book_name_match = re.search(r'"book_name": "([^"]+)"', response)
    final_score_match = re.search(r'"final_score": (\d+)', response)
    incorrect_answers_count_match = re.search(r'"incorrect_answers_count": (\d+)', response)

    student_name = student_name_match.group(1) if student_name_match else ''
    book_name = book_name_match.group(1) if book_name_match else ''
    final_score = int(final_score_match.group(1)) if final_score_match else 0
    incorrect_answers_count = int(incorrect_answers_count_match.group(1)) if incorrect_answers_count_match else 0

    # Extract detailed review
    detailed_review = []
    questions_matches = re.findall(
        r'"question_number": (\d+),.*?"correct_answer": "([^"]+)"', response, re.DOTALL)

    for match in questions_matches:
        question_number = int(match[0])
        correct_version = match[1]

        question = {
            'question_number': question_number,
            'status': 'Incorrect',
            'correct_version': correct_version
        }
        detailed_review.append(question)

    # Create structured response
    structured_response = {
        'student_name': student_name,
        'book_name': book_name,
        'final_score': final_score,
        'incorrect_answers': incorrect_answers_count,
        'detailed_review': detailed_review
    }

    return structured_response

# automatically save
def save_review_to_db(response_data,user):
    # Create and save the StudentReview instance
    student_review = StudentReview(
        user = user,
        student_name=response_data['student_name'],
        book_name=response_data['book_name'],
        final_score=response_data['final_score'],
        incorrect_answers_count=response_data['incorrect_answers']
    )
    student_review.save()

    # Create and save the QuestionDetail instances
    for detail in response_data['detailed_review']:
        question_detail = QuestionDetail(
            user = user,
            student_review=student_review,
            question_number=detail['question_number'],
            status=detail['status'],
            correct_version=detail['correct_version']
        )
        question_detail.save()

# Define the response string
# response = '''
# {
# "review": {
# "student_name": "ali axmed",
# "book_name":"Django for beginners",
# "results": {
# "final_score": 7,
# "incorrect_answers_count": 3,
# "incorrect_answers_details": [
# {
# "question_number": 2,
# "reason": "The answer does not outline all the necessary steps for installing Django, such as creating a virtual environment and activating it.",
# "correct_answer": "1. Ensure Python is installed.\\n2. Open a command prompt and run 'pip install django'.\\n3. Optionally, create and activate a virtual environment.\\n4. Confirm the installation by running 'django-admin --version'. ."
# },
# {
# "question_number": 4,
# "reason": "The command provided is incorrect; the correct command to start the development server is 'python manage.py runserver'.",
# "correct_answer": "You start the development server by running 'python manage.py runserver' ."
# },
# {
# "question_number": 9,
# "reason": "Templates are not used for storing static files; they are used to define the HTML structure of web pages.",
# "correct_answer": "Templates in Django are used to generate dynamic HTML content ."
# }
# ]
# }
# }
# }
# '''
# Extract and structure the response
# structured_data = extract_details_from_string(response)

# print(structured_data)
