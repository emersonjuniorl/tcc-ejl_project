import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from decimal import Decimal

from .models import Project, Dimension, Question, Assessment, Answer
from .utils import compute_scores, build_recommendations

User = get_user_model()


class CoreModelsTest(TestCase):
    """Test cases for core models"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.dimension = Dimension.objects.create(
            code='TEST_DIM',
            title='Test Dimension',
            framework='PMBOK'
        )
        
        self.question = Question.objects.create(
            dimension=self.dimension,
            text='Test question?',
            weight=1.0,
            order=1
        )
        
        self.project = Project.objects.create(
            name='Test Project',
            description='Test project description',
            owner=self.user
        )

    def test_project_creation(self):
        """Test project creation and string representation"""
        self.assertEqual(str(self.project), 'Test Project')
        self.assertEqual(self.project.owner, self.user)
        self.assertIsNotNone(self.project.created_at)
        self.assertIsNotNone(self.project.updated_at)

    def test_dimension_creation(self):
        """Test dimension creation and string representation"""
        self.assertEqual(str(self.dimension), 'PMBOK - Test Dimension')
        self.assertEqual(self.dimension.framework, 'PMBOK')

    def test_question_creation(self):
        """Test question creation and string representation"""
        self.assertEqual(str(self.question), 'Test question?')
        self.assertEqual(self.question.dimension, self.dimension)
        self.assertEqual(self.question.weight, 1.0)

    def test_assessment_creation(self):
        """Test assessment creation"""
        assessment = Assessment.objects.create(
            project=self.project,
            evaluator=self.user
        )
        self.assertEqual(assessment.project, self.project)
        self.assertEqual(assessment.evaluator, self.user)
        self.assertEqual(assessment.compliance_score, 0.0)
        self.assertEqual(assessment.maturity_score, 0.0)

    def test_answer_creation(self):
        """Test answer creation and unique constraint"""
        assessment = Assessment.objects.create(
            project=self.project,
            evaluator=self.user
        )
        
        answer = Answer.objects.create(
            assessment=assessment,
            question=self.question,
            value=4
        )
        
        self.assertEqual(answer.value, 4)
        self.assertEqual(answer.assessment, assessment)
        self.assertEqual(answer.question, self.question)


class CoreUtilsTest(TestCase):
    """Test cases for utility functions"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.dimension = Dimension.objects.create(
            code='TEST_DIM',
            title='Test Dimension',
            framework='PMBOK'
        )
        
        self.question1 = Question.objects.create(
            dimension=self.dimension,
            text='Question 1?',
            weight=2.0,
            order=1
        )
        
        self.question2 = Question.objects.create(
            dimension=self.dimension,
            text='Question 2?',
            weight=1.0,
            order=2
        )
        
        self.project = Project.objects.create(
            name='Test Project',
            description='Test project description',
            owner=self.user
        )
        
        self.assessment = Assessment.objects.create(
            project=self.project,
            evaluator=self.user
        )

    def test_compute_scores_basic(self):
        """Test basic score computation"""
        # Create answers with values 4 and 3
        Answer.objects.create(
            assessment=self.assessment,
            question=self.question1,
            value=4
        )
        Answer.objects.create(
            assessment=self.assessment,
            question=self.question2,
            value=3
        )
        
        scores = compute_scores(self.assessment)
        
        # Expected: weighted average of (4*2 + 3*1) / (2+1) = 11/3 = 3.67
        # Normalized to 100: (3.67/5) * 100 = 73.33
        expected_compliance = round((11/3) / 5 * 100, 2)
        self.assertEqual(scores['compliance'], expected_compliance)
        self.assertEqual(scores['maturity'], expected_compliance)

    def test_compute_scores_edge_cases(self):
        """Test score computation with edge cases"""
        # Test with no answers
        scores = compute_scores(self.assessment)
        self.assertEqual(scores['compliance'], 0.0)
        self.assertEqual(scores['maturity'], 0.0)
        
        # Test with extreme values
        Answer.objects.create(
            assessment=self.assessment,
            question=self.question1,
            value=10  # Should be clamped to 5
        )
        
        scores = compute_scores(self.assessment)
        self.assertEqual(scores['compliance'], 100.0)  # 5/5 * 100

    def test_build_recommendations(self):
        """Test recommendation generation"""
        # Low compliance
        recs = build_recommendations(30.0, 30.0)
        self.assertIn("Formalize planejamento", recs[0])
        self.assertIn("Implemente controles mínimos", recs[1])
        
        # Medium compliance
        recs = build_recommendations(60.0, 60.0)
        self.assertIn("Aprimore gestão de mudanças", recs[0])
        self.assertIn("Fortaleça governança", recs[1])
        
        # High compliance
        recs = build_recommendations(85.0, 85.0)
        self.assertIn("Consolide lições aprendidas", recs[0])
        
        # Low maturity
        recs = build_recommendations(80.0, 40.0)
        self.assertIn("Priorize entregas incrementais", recs[-1])


class CoreAPITest(APITestCase):
    """Test cases for API endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.dimension = Dimension.objects.create(
            code='TEST_DIM',
            title='Test Dimension',
            framework='PMBOK'
        )
        
        self.question = Question.objects.create(
            dimension=self.dimension,
            text='Test question?',
            weight=1.0,
            order=1
        )
        
        self.project = Project.objects.create(
            name='Test Project',
            description='Test project description',
            owner=self.user
        )

    def test_health_endpoint(self):
        """Test health endpoint"""
        response = self.client.get('/api/health/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'status': 'ok'})

    def test_questions_endpoint(self):
        """Test questions endpoint"""
        response = self.client.get('/api/questions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        
        question_data = response.json()[0]
        self.assertEqual(question_data['text'], 'Test question?')
        self.assertEqual(question_data['dimension'], self.dimension.id)

    def test_dimensions_endpoint(self):
        """Test dimensions endpoint"""
        response = self.client.get('/api/dimensions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        
        dimension_data = response.json()[0]
        self.assertEqual(dimension_data['title'], 'Test Dimension')
        self.assertEqual(dimension_data['framework'], 'PMBOK')

    def test_projects_endpoint_authenticated(self):
        """Test projects endpoint with authentication"""
        self.client.force_authenticate(user=self.user)
        
        # Test GET
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        
        # Test POST
        project_data = {
            'name': 'New Project',
            'description': 'New project description'
        }
        response = self.client.post('/api/projects/', project_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        new_project = response.json()
        self.assertEqual(new_project['name'], 'New Project')
        self.assertEqual(new_project['owner']['username'], 'testuser')

    def test_projects_endpoint_unauthenticated(self):
        """Test projects endpoint without authentication"""
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Changed from 401 to 403
        
        project_data = {
            'name': 'New Project',
            'description': 'New project description'
        }
        response = self.client.post('/api/projects/', project_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Changed from 401 to 403

    def test_assessments_endpoint_authenticated(self):
        """Test assessments endpoint with authentication"""
        self.client.force_authenticate(user=self.user)
        
        # Test GET
        response = self.client.get('/api/assessments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)  # No assessments yet
        
        # Test POST - need to create a project first
        project_data = {
            'name': 'Assessment Test Project',
            'description': 'Project for assessment testing'
        }
        project_response = self.client.post('/api/projects/', project_data)
        self.assertEqual(project_response.status_code, status.HTTP_201_CREATED)
        project_id = project_response.json()['id']
        
        # First, test creating assessment without answers
        basic_assessment_data = {
            'project': project_id,
        }
        basic_response = self.client.post('/api/assessments/', basic_assessment_data)
        print(f"Basic assessment response: {basic_response.status_code}")
        print(f"Basic assessment content: {basic_response.content}")
        
        # Now test with answers
        assessment_data = {
            'project': project_id,
            'answers': [
                {
                    'question': self.question.id,
                    'value': 4
                }
            ]
        }
        response = self.client.post('/api/assessments/', assessment_data)
        
        # Debug: print response details if it fails
        if response.status_code != status.HTTP_201_CREATED:
            print(f"Response status: {response.status_code}")
            print(f"Response content: {response.content}")
            print(f"Assessment data sent: {assessment_data}")
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        assessment = response.json()
        self.assertEqual(assessment['project'], project_id)
        self.assertGreater(assessment['compliance_score'], 0)
        self.assertGreater(assessment['maturity_score'], 0)

    def test_assessment_report_endpoint(self):
        """Test assessment report endpoint"""
        self.client.force_authenticate(user=self.user)
        
        # Create assessment with answers
        assessment = Assessment.objects.create(
            project=self.project,
            evaluator=self.user
        )
        
        Answer.objects.create(
            assessment=assessment,
            question=self.question,
            value=4
        )
        
        # Update scores
        scores = compute_scores(assessment)
        assessment.compliance_score = scores['compliance']
        assessment.maturity_score = scores['maturity']
        assessment.save()
        
        # Test report endpoint
        response = self.client.get(f'/api/assessments/{assessment.id}/report/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        report = response.json()
        self.assertEqual(report['assessment_id'], assessment.id)
        self.assertEqual(report['project'], self.project.name)
        self.assertIn('scores', report)
        self.assertIn('recommendations', report)
        self.assertGreater(len(report['recommendations']), 0)


@pytest.mark.integration
class CoreIntegrationTest(APITestCase):
    """Integration tests for complete workflows"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        # Create test data
        self.dimension = Dimension.objects.create(
            code='TEST_DIM',
            title='Test Dimension',
            framework='PMBOK'
        )
        
        self.question = Question.objects.create(
            dimension=self.dimension,
            text='Test question?',
            weight=1.0,
            order=1
        )

    def test_complete_assessment_workflow(self):
        """Test complete assessment workflow from project creation to report"""
        # 1. Create project
        project_data = {
            'name': 'Integration Test Project',
            'description': 'Project for integration testing'
        }
        project_response = self.client.post('/api/projects/', project_data)
        self.assertEqual(project_response.status_code, status.HTTP_201_CREATED)
        project_id = project_response.json()['id']
        
        # 2. Create assessment
        assessment_data = {
            'project': project_id,
            'answers': [
                {
                    'question': self.question.id,
                    'value': 4
                }
            ]
        }
        assessment_response = self.client.post('/api/assessments/', assessment_data)
        self.assertEqual(assessment_response.status_code, status.HTTP_201_CREATED)
        assessment_id = assessment_response.json()['id']
        
        # 3. Get report
        report_response = self.client.get(f'/api/assessments/{assessment_id}/report/')
        self.assertEqual(report_response.status_code, status.HTTP_200_OK)
        
        report = report_response.json()
        self.assertEqual(report['project'], 'Integration Test Project')
        self.assertIn('scores', report)
        self.assertIn('recommendations', report)
        
        # 4. Verify scores were calculated
        assessment = Assessment.objects.get(id=assessment_id)
        self.assertGreater(assessment.compliance_score, 0)
        self.assertGreater(assessment.maturity_score, 0)
