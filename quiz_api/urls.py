from django.urls import path
from .views import (UserTestListView, UserTestQuestionListView, UserTestChoicesListView, UserTestChoiceAnswerListView,
CreateTestView, CreateChoiceAnswerView)

urlpatterns = [
    path('user_tests/', UserTestListView.as_view(), name='user-test-view'),
    path('user_test_questions/', UserTestQuestionListView.as_view(), name='user-test-question-view'),
    path('user_test_choices/', UserTestChoicesListView.as_view(), name='user-test-choice-view'),
    path('user_test_choiceanswers/', UserTestChoiceAnswerListView.as_view(), name='user-test-choiceanswer-view'),
    path('createtest/<int:note_id>/', CreateTestView.as_view(), name='create-test-view'),
    path('choiceanswers/<int:choice_id>/', CreateChoiceAnswerView.as_view(), name='choiceanswer-create'),
    
]
