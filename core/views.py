from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, permissions, decorators, response
from .models import Project, Dimension, Question, Assessment
from .serializers import (
    ProjectSerializer,
    DimensionSerializer,
    QuestionSerializer,
    AssessmentSerializer,
)
from .utils import compute_scores, build_recommendations


def health(request):
    return JsonResponse({"status": "ok"})


def questionnaire(request):
    return render(request, 'core/questionnaire.html')


@csrf_exempt
def create_demo_project(request):
    """Create a demo project for public use"""
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            
            # Create a demo project with a default user
            from django.contrib.auth import get_user_model
            User = get_user_model()
            
            # Get or create a demo user
            demo_user, created = User.objects.get_or_create(
                username='demo_user',
                defaults={
                    'email': 'demo@example.com',
                    'first_name': 'Demo',
                    'last_name': 'User'
                }
            )
            
            # Create the project
            project = Project.objects.create(
                name='Projeto Demo - ' + data.get('name', 'Avaliação'),
                description='Projeto criado automaticamente para demonstração',
                owner=demo_user
            )
            
            return JsonResponse({
                'id': project.id,
                'name': project.name,
                'description': project.description
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def create_demo_assessment(request):
    """Create a demo assessment for public use"""
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            
            # Get the project
            project_id = data.get('project')
            answers_data = data.get('answers', [])
            
            if not project_id or not answers_data:
                return JsonResponse({'error': 'Project ID and answers are required'}, status=400)
            
            project = Project.objects.get(id=project_id)
            
            # Create assessment
            assessment = Assessment.objects.create(
                project=project,
                evaluator=project.owner  # Use project owner as evaluator
            )
            
            # Create answers
            from .models import Answer, Question
            for answer_data in answers_data:
                question = Question.objects.get(id=answer_data['question'])
                Answer.objects.create(
                    assessment=assessment,
                    question=question,
                    value=answer_data['value']
                )
            
            # Compute scores
            scores = compute_scores(assessment)
            assessment.compliance_score = scores["compliance"]
            assessment.maturity_score = scores["maturity"]
            assessment.save()
            
            return JsonResponse({
                'id': assessment.id,
                'project': project.name,
                'compliance_score': assessment.compliance_score,
                'maturity_score': assessment.maturity_score
            })
            
        except Project.DoesNotExist:
            return JsonResponse({'error': 'Project not found'}, status=404)
        except Question.DoesNotExist:
            return JsonResponse({'error': 'Question not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def get_demo_report(request, assessment_id):
    """Get assessment report for demo purposes"""
    try:
        assessment = Assessment.objects.get(id=assessment_id)
        scores = {"compliance": assessment.compliance_score, "maturity": assessment.maturity_score}
        recs = build_recommendations(scores["compliance"], scores["maturity"])
        
        return JsonResponse({
            "assessment_id": assessment.id,
            "project": assessment.project.name,
            "scores": scores,
            "recommendations": recs,
        })
    except Assessment.DoesNotExist:
        return JsonResponse({'error': 'Assessment not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().select_related("owner")
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DimensionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Dimension.objects.all().prefetch_related("questions")
    serializer_class = DimensionSerializer
    permission_classes = [permissions.AllowAny]


class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Question.objects.filter(is_active=True)
    serializer_class = QuestionSerializer
    permission_classes = [permissions.AllowAny]


class AssessmentViewSet(viewsets.ModelViewSet):
    queryset = Assessment.objects.all().select_related("project", "evaluator")
    serializer_class = AssessmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    @decorators.action(detail=True, methods=["get"], url_path="report")
    def report(self, request, pk=None):
        assessment = self.get_object()
        scores = {"compliance": assessment.compliance_score, "maturity": assessment.maturity_score}
        recs = build_recommendations(scores["compliance"], scores["maturity"])
        return response.Response({
            "assessment_id": assessment.id,
            "project": assessment.project.name,
            "scores": scores,
            "recommendations": recs,
        })

# Create your views here.
