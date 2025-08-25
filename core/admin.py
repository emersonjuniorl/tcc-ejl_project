from django.contrib import admin
from .models import Project, Dimension, Question, Assessment, Answer


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "created_at")
    search_fields = ("name", "description", "owner__username")


@admin.register(Dimension)
class DimensionAdmin(admin.ModelAdmin):
    list_display = ("code", "framework", "title")
    list_filter = ("framework",)
    search_fields = ("code", "title")


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "dimension", "order", "is_active")
    list_filter = ("dimension", "is_active")
    search_fields = ("text",)


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ("id", "project", "evaluator", "compliance_score", "maturity_score", "created_at")
    inlines = [AnswerInline]

# Register your models here.
