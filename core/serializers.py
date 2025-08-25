from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Project, Dimension, Question, Assessment, Answer
from .utils import compute_scores


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "username", "first_name", "last_name", "email"]


class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Project
        fields = ["id", "name", "description", "owner", "created_at", "updated_at"]


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "dimension", "text", "weight", "order", "is_active"]


class DimensionSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Dimension
        fields = ["id", "code", "title", "framework", "questions"]


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ["id", "question", "value"]


class AssessmentSerializer(serializers.ModelSerializer):
    answers = serializers.ListField(write_only=True)

    class Meta:
        model = Assessment
        fields = [
            "id",
            "project",
            "evaluator",
            "created_at",
            "compliance_score",
            "maturity_score",
            "answers",
        ]
        read_only_fields = ["compliance_score", "maturity_score", "created_at"]

    def create(self, validated_data):
        answers_data = validated_data.pop("answers", [])
        
        # If no evaluator is provided, use the project owner
        if 'evaluator' not in validated_data:
            validated_data['evaluator'] = validated_data['project'].owner
        
        assessment = Assessment.objects.create(**validated_data)
        
        # Create answers - handle both string and dict formats
        for answer_data in answers_data:
            if isinstance(answer_data, str):
                # Try to parse string as dict
                try:
                    import ast
                    parsed_data = ast.literal_eval(answer_data)
                    if isinstance(parsed_data, dict):
                        # Convert question ID to Question instance
                        question_id = parsed_data.get('question')
                        question = Question.objects.get(id=question_id)
                        Answer.objects.create(
                            assessment=assessment,
                            question=question,
                            value=parsed_data.get('value')
                        )
                    else:
                        print(f"Invalid parsed data: {parsed_data}")
                except Exception as e:
                    print(f"Failed to parse string '{answer_data}': {e}")
            elif isinstance(answer_data, dict):
                # Convert question ID to Question instance
                question_id = answer_data.get('question')
                question = Question.objects.get(id=question_id)
                Answer.objects.create(
                    assessment=assessment,
                    question=question,
                    value=answer_data.get('value')
                )
            else:
                print(f"Skipping invalid answer data: {answer_data}")
        
        # Compute and persist scores
        scores = compute_scores(assessment)
        assessment.compliance_score = scores["compliance"]
        assessment.maturity_score = scores["maturity"]
        assessment.save(update_fields=["compliance_score", "maturity_score"])
        
        return assessment

