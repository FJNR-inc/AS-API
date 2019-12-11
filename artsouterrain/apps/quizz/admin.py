from django.contrib import admin
from .models import *


class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'label',
        'page',
        'type',
        'index',
    )
    list_filter = (
        'page',
    )


class ChoiceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'label',
        'question',
        'index',
    )


class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'question',
        'submission',
    )
    list_filter = (
        'question',
        'submission',
        'submission__user',
    )


class SubmissionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'completed',
        'created',
        'updated',
    )
    list_filter = (
        'user',
        'completed'
    )


admin.site.register(Assessment)
admin.site.register(Page)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Submission, SubmissionAdmin)
