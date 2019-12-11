from django.urls import path
from rest_framework.routers import SimpleRouter
from django.conf.urls import include

from . import views


class OptionalSlashSimpleRouter(SimpleRouter):
    """ Subclass of SimpleRouter to make the trailing slash optional """
    def __init__(self, *args, **kwargs):
        super(SimpleRouter, self).__init__(*args, **kwargs)
        self.trailing_slash = '/?'


router = OptionalSlashSimpleRouter()
router.register('assessments', views.AssessmentViewSet)
router.register('pages', views.PageViewSet)
router.register('questions', views.QuestionViewSet)
router.register('choices', views.ChoiceViewSet)
router.register('answers', views.AnswerViewSet)
router.register('submissions', views.SubmissionViewSet)

urlpatterns = [
    path('', include(router.urls)),  # includes router generated URL
]
