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

import base64
import requests

# OpenAI API Key
api_key = "sk-proj-GmtcP1oqpnaWh0lEuuccT3BlbkFJDAqSxmdbrItZcFJGQwiP"

import base64

def analyze_images(image_streams):
    def encode_image(image_stream):
        return base64.b64encode(image_stream).decode('utf-8')

    # Encode all images
    base64_images = [encode_image(image_stream) for image_stream in image_streams]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # Create the content payload with multiple images
    content = [
        {
            "type": "text",
            "text": '''
                    Please transcribe all the content from the exam paper displayed in the image. Include the student_name ,subject name , complete exam questions and the answers provided by the students. This transcription is intended for another LLM to grade the exams, so it is vital to include all essential details. Organize your response to ensure clarity and readability, covering various types of exam sections as outlined below:

                    - Multiple Choice Questions:

                    Present the question, the options (labeled as a, b, c, etc.), and the student's chosen answer.

                    - Short Answer Questions:

                    Include the question and the student's full response.
                    
                    - Essay Questions:

                    Provide the question and the student's complete essay response.
                    
                    - Math Questions:

                    Include the question and the student's final answer. For questions involving calculations, only state the final answer under 'Answers of Direct Math Questions.'
                    
                    - True/False Questions:

                    State the question and the student's selected answer.
                    
                    - Fill-in-the-Blank Questions:

                    Include the question with the blanks and the student's filled-in responses.
                    
                    - Matching Questions:

                    List the instructions and the pairs matched by the student.
                    
                    - Diagram Questions:

                    Include the question and describe the student's diagram or sketch in detail. If the diagram is intricate, acknowledge its presence and outline its key elements.
                    
                    - Complete the Following Questions:

                    Include the incomplete statement, specify what the student completed, and what was originally there.

                    If multiple images of the exam paper are provided, ensure that all sections and pages are transcribed. Please refrain from adding any additional introductory or concluding remarks. Structure your response logically for easy comprehension, and only transcribe the student's responses without making any corrections or alterations.
                    
                    '''
        }
    ] + [
        {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
        }
        for base64_image in base64_images
    ]

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": content
            }
        ]
    }

    # Send the request to the OpenAI API
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    return response.json()['choices'][0]['message']['content']

# Example usage
# image_paths = ["./exm0.jpg", "./exm1.jpg","./exm2.jpg","./exm3.jpg"]
# response_text = analyze_images(image_paths)
# print(response_text)
