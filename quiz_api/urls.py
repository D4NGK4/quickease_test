from django.urls import path
from .views import (UserTestListView, 
                    CreateTestView,
                    UserTestRetrieveUpdateDestroyView,
                    
                    UserTestQuestionListView,
                    CreateTestQuestionView,
                    UserTestQuestionDetailView,
                    
                    UserTestChoicesListView,
                    CreateQuestionChoicesView,
                    UserTestChoiceDetailView,
                    
                    ChoiceAnswerListView,
                    CreateChoiceAnswerView,
                    ChoiceAnswerDetailView,
                    
                    QuestionByNoteView,
                    ChoicesByNoteView,
                    AnswerByQuestionView,
                    AnswerByNoteView
)

urlpatterns = [
    # User Tests
    path('usertests/', UserTestListView.as_view(), name='usertest-list-create'),
    path('usertest-create/<int:note_id>/', CreateTestView.as_view(), name='usertest-create'),
    path('usertest-detail/<int:pk>/', UserTestRetrieveUpdateDestroyView.as_view(), name='usertest-detail'),
    
    # Test Questions
    # Use usertest/questions/0/ to show all questions
    path('usertest/questions/<int:note_id>/', UserTestQuestionListView.as_view(), name='user-test-questions'),
    path('questions/create/<note_id>/', CreateTestQuestionView.as_view(), name='questions-create'),
    path('question/<int:question_id>/', UserTestQuestionDetailView.as_view(), name='question-detail'),
    
    # Question Choices
    # We can filter choices by question using the question_id, put 0 to get all choices
    # use usertest/choices/0/ to show all choices
     path('usertest/choices/<int:question_id>/', UserTestChoicesListView.as_view(), name='user-test-choices'),
     path('usertest/choice-create/<int:question_id>/', CreateQuestionChoicesView.as_view(), name='user-test-choice-create'),
     path('usertest/choice-detail/<int:choice_id>/', UserTestChoiceDetailView.as_view(), name='user-test-choice-detail'),
     
    # Choices Answer
    # use usertest/choice-answers/0/ to show all choices
    path('choice-answers/<int:choice_id>/', ChoiceAnswerListView.as_view(), name='choice-answer-list'),
    path('choice-answer/create/<int:choice_id>/', CreateChoiceAnswerView.as_view(), name='choice-answer-create'),
    path('choice-answer/<int:choice_id>/', ChoiceAnswerDetailView.as_view(), name='choice-answer-detail'),
    
    #Custom Views
    path('answer-by-question/<int:question_id>/', AnswerByQuestionView.as_view(), name='answer-by-question'),
    path('answer-by-note/<int:note_id>/', AnswerByNoteView.as_view(), name='answer-by-note'),
    path('question-by-note/<int:note_id>/', QuestionByNoteView.as_view(), name='question-by-note'),
    path('choices-by-note/<int:note_id>/', ChoicesByNoteView.as_view(), name='choices-by-note'),
]
