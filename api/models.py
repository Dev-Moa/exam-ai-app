from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class StudentReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    student_name = models.CharField(max_length=100)
    book_name = models.CharField(max_length=100)
    final_score = models.IntegerField()
    incorrect_answers_count = models.IntegerField()

class QuestionDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    student_review = models.ForeignKey(StudentReview, on_delete=models.CASCADE, related_name='detailed_review')
    question_number = models.IntegerField()
    status = models.CharField(max_length=50)
    correct_version = models.TextField()