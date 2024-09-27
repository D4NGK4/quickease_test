from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import UserTest, TestQuestion, TestChoices, ChoiceAnswer
from .serializers import (  UserTestSerializer,
                            TestQuestionSerializer,
                            TestChoicesSerializer,
                            ChoiceAnswerSerializer,
)
from summarizer_api.models import UserNotes  

#Normal VIEWS

class UserTestListView(generics.ListAPIView):
    serializer_class = UserTestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserTest.objects.filter(note__user=self.request.user)
    
class UserTestQuestionListView(generics.ListAPIView):
    serializer_class = TestQuestionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        note_id = self.kwargs.get('note_id')
        user = self.request.user
        
        if note_id != 0:
            note = get_object_or_404(UserNotes, id=note_id, user=self.request.user)
            user_test = get_object_or_404(UserTest, note=note)
            return TestQuestion.objects.filter(test=user_test)
        return TestQuestion.objects.filter(test__note__user=user)
        

class UserTestChoicesListView(generics.ListAPIView):
    serializer_class = TestChoicesSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        question_id = self.kwargs.get('question_id')
        user = self.request.user

        if question_id != 0:
            user_question = get_object_or_404(TestQuestion,id=question_id,test__note__user=self.request.user)
            return TestChoices.objects.filter(question=user_question)
        else:
            return TestChoices.objects.filter(question__test__note__user=user)
    

class ChoiceAnswerListView(generics.ListAPIView):
    serializer_class = ChoiceAnswerSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        choice_id = self.kwargs.get('choice_id')
        user = self.request.user
        if choice_id != 0: 
            return ChoiceAnswer.objects.filter(answer__question__id=choice_id)
        return ChoiceAnswer.objects.filter(answer__question__test__note__user=user)
        

#create views

class CreateTestView(generics.CreateAPIView):
    serializer_class = UserTestSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, note_id):
        note_object = get_object_or_404(UserNotes, id=note_id, user=request.user)
        serializer = UserTestSerializer(data=request.data)

        if UserTest.objects.filter(note=note_object).exists():
            return Response({"status": "error", "message": "Test already exists for this note."}, status=status.HTTP_400_BAD_REQUEST)
        
        if serializer.is_valid():
            serializer.save(note=note_object)
            return Response({"status": "success", "test": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CreateTestQuestionView(generics.CreateAPIView):
    serializer_class = TestQuestionSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        note_id = self.kwargs.get('note_id')
        if note_id == '0':
            raise serializers.ValidationError("Cannot create a question without a specific note.")
        try:
            note_id_int = int(note_id)
        except ValueError:
            raise serializers.ValidationError("Invalid note ID.")
        note = get_object_or_404(UserNotes, id=note_id_int, user=self.request.user)
        user_test, created = UserTest.objects.get_or_create(note=note)
        serializer.save(test=user_test)
    
class CreateQuestionChoicesView(generics.CreateAPIView):
    serializer_class = TestChoicesSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request, question_id):
        question_object = get_object_or_404(TestQuestion, id=question_id, test__note__user=request.user)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(question=question_object)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
class CreateChoiceAnswerView(generics.CreateAPIView):
    serializer_class = ChoiceAnswerSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, choice_id):
        try:
            choice_id_int = int(choice_id)
        except (TypeError, ValueError):
            return Response({"detail": "Invalid choice ID."}, status=status.HTTP_400_BAD_REQUEST)

        test_choice = get_object_or_404(
            TestChoices,
            id=choice_id_int,
            question__test__note__user=request.user
        )
        if ChoiceAnswer.objects.filter(
            answer__question=test_choice.question,
            answer__question__test__note__user=request.user
        ).exists():
            return Response({"Error": "You have already answered this question."}, status=status.HTTP_400_BAD_REQUEST)
        choice_answer = ChoiceAnswer.objects.create(answer=test_choice)
        serializer = ChoiceAnswerSerializer(choice_answer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
#retrieveupdatedestroy views

class UserTestRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserTestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserTest.objects.filter(note__user=self.request.user)
    
class UserTestChoiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TestChoicesSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'choice_id'

    def get_queryset(self):
        return TestChoices.objects.filter(question__test__note__user=self.request.user)

class UserTestQuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TestQuestionSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'question_id'
    
    def get_queryset(self):
        return TestQuestion.objects.filter(test__note__user=self.request.user)
             
class ChoiceAnswerDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChoiceAnswerSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'answer__id'
    lookup_url_kwarg = 'choice_id'

    def get_queryset(self):
        return ChoiceAnswer.objects.filter(
            answer__question__test__note__user=self.request.user
        )
    
#Custom Views

class QuestionByNoteView(generics.ListAPIView):
    serializer_class = TestQuestionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        note_id = self.kwargs.get('note_id')
        user = self.request.user
        if note_id != 0:
            return TestQuestion.objects.filter(test__note__id=note_id)
        return TestQuestion.objects.filter(test__note__user=user)
    

class AnswerByQuestionView(generics.ListAPIView):
    serializer_class = ChoiceAnswerSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        question_id = self.kwargs.get('question_id')
        user = self.request.user
        if question_id != 0:
            return ChoiceAnswer.objects.filter(answer__question__id=question_id)
        return ChoiceAnswer.objects.filter(answer__question__test__note__user=user)

class AnswerByNoteView(generics.ListAPIView):
    serializer_class = ChoiceAnswerSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        note_id = self.kwargs.get('note_id')
        user = self.request.user
        if note_id != 0:
            return ChoiceAnswer.objects.filter(answer__question__test__note__id=note_id)
        return ChoiceAnswer.objects.filter(answer__question__test__note__user=user)
    
class ChoicesByNoteView(generics.ListAPIView):
    serializer_class = TestChoicesSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        note_id = self.kwargs.get('note_id')
        user = self.request.user
        if note_id != 0:
            return TestChoices.objects.filter(question__test__note__id=note_id)
        return TestChoices.objects.filter(question__test__note__user=user)