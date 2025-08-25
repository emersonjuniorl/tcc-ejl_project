from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class Dimension(models.Model):
    code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=200)
    framework = models.CharField(max_length=50, choices=[
        ('PMBOK', 'PMBOK'),
        ('HCMBOK', 'HCMBOK'),
        ('PRINCE', 'PRINCE'),
        ('COMPLIANCE', 'COMPLIANCE'),
    ])

    def __str__(self) -> str:
        return f"{self.framework} - {self.title}"


class Question(models.Model):
    dimension = models.ForeignKey(Dimension, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    weight = models.FloatField(default=1.0)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self) -> str:
        return self.text[:80]


class Assessment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='assessments')
    evaluator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    compliance_score = models.FloatField(default=0.0)
    maturity_score = models.FloatField(default=0.0)

    def __str__(self) -> str:
        return f"Assessment {self.id} - {self.project.name}"


class Answer(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    value = models.IntegerField()

    class Meta:
        unique_together = ('assessment', 'question')


# Create your models here.
