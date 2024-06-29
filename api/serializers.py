from rest_framework import serializers
from .models import StudentReview
from django.contrib.auth.models import User


class VisionExamSerializer(serializers.Serializer):
    imgs = serializers.ImageField()

class CorrectExamSerializer(serializers.Serializer):
    original_file = serializers.FileField()
    student_files = serializers.ListField(
        child=serializers.ImageField(), 
        allow_empty=False
    )

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'username','is_superuser', 'password')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class StudentMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentReview
        fields = '__all__'
        read_only_fields = ('id',)
    
class GenerateExamSerializer(serializers.Serializer):
    file = serializers.FileField()
    exam_chapters =  serializers.CharField(max_length=100)
    exam_parts = serializers.ListField(
        child=serializers.CharField(max_length=100)
    )
    each_part_question_numbers = serializers.CharField(max_length=100)
    exam_difficulty = serializers.ChoiceField(choices=["Easy", "Medium", "Hard"])
    exam_level = serializers.ChoiceField(choices=["Primary", "High School", "University"])

