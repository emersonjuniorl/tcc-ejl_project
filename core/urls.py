from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'projects', views.ProjectViewSet, basename='project')
router.register(r'dimensions', views.DimensionViewSet, basename='dimension')
router.register(r'questions', views.QuestionViewSet, basename='question')
router.register(r'assessments', views.AssessmentViewSet, basename='assessment')


urlpatterns = [
    path('health/', views.health, name='health'),
    path('questionnaire/', views.questionnaire, name='questionnaire'),
    path('demo-project/', views.create_demo_project, name='demo_project'),
    path('demo-assessment/', views.create_demo_assessment, name='demo_assessment'),
    path('demo-report/<int:assessment_id>/', views.get_demo_report, name='demo_report'),
    path('', include(router.urls)),
]


