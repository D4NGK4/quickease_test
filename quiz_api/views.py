from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import UserTest, TestQuestion, TestChoices
from summarizer_api.models import UserNotes
from .serializers import UserTestSerializer, TestQuestionSerializer, TestChoicesSerializer, ChoiceAnswerSerializer
from .question_create import generate_questions
from .choice_create import generate_choices
import json

#GET METHODS
# Generic Views
class UserTestListView(generics.ListAPIView):
    serializer_class = UserTestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return UserTest.objects.filter(note__user=user)
    
# FIX THIS
class UserTestQuestionListView(generics.ListAPIView):
    serializer_class = TestQuestionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.test
        test = generics.get_object_or_404(UserTest, note_id=user)
        return TestQuestion.objects.filter(id=test)
    
#TODO
class UserTestChoicesListView(generics.ListAPIView):
    serializer_class = TestChoicesSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return TestChoices.objects.filter(user=self.request.user)
    
class UserTestChoiceAnswerListView(generics.ListAPIView):
    serializer_class = TestChoicesSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return TestChoices.objects.filter(user=self.request.user)
    
#PUT METHODS

    
#POST METHODS
# Create Test
class CreateTestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, note_id):
        note = generics.get_object_or_404(UserNotes, id=note_id)

        if not note.notesummary:
            return Response(
                {"status": "error", "message": "Note summary is empty."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if UserTest.objects.filter(note_id=note_id).exists():
            return Response(
                {"status": "error", "message": "Test already exists for this note."},
                status=status.HTTP_400_BAD_REQUEST
            )

        JSON_DATA = generate_questions(note.notesummary)

        try:
            question_data = json.loads(JSON_DATA)

            if not isinstance(question_data, list):
                return Response(
                    {"status": "error", "message": "Expected a list of questions but got something else."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            usertest = UserTest.objects.create(
                note=note,
                TestScore=0,
                TestTotalScore=0
            )

            question_list = []
            for item in question_data:
                if not isinstance(item, dict):
                    return Response(
                        {"status": "error", "message": "Invalid question format. Expected a dictionary."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                question_text = item.get('Question', '')

                question_instance = TestQuestion.objects.create(
                    test=usertest,
                    TestQuestion=question_text
                )
                question_list.append(TestQuestionSerializer(question_instance).data)

                question_choices_data = generate_choices(question_text)
                choices_data = json.loads(question_choices_data)

                if not isinstance(choices_data, list):
                    return Response(
                        {"status": "error", "message": "Expected a list of choices but got something else."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                for choice in choices_data:
                    if not isinstance(choice, dict):
                        return Response(
                            {"status": "error", "message": "Invalid choice format. Expected a dictionary."},
                            status=status.HTTP_400_BAD_REQUEST
                        )

                    TestChoices.objects.create(
                        question=question_instance,
                        item_choice_text=choice.get('choice', ''),
                        isAnswer=choice.get('isAnswer', False)
                    )

            return Response({"status": "success", "questions": question_list}, status=status.HTTP_201_CREATED)

        except json.JSONDecodeError:
            return Response(
                {"status": "error", "message": "Failed to decode JSON response."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"status": "error", "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

# Create Choice Answer
class CreateChoiceAnswerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, choice_id):
        choice = generics.get_object_or_404(TestChoices, id=choice_id)

        if ChoiceAnswer.objects.filter(answer=choice).exists():
            return Response(
                {"status": "error", "message": "Answer already exists for this choice."},
                status=status.HTTP_400_BAD_REQUEST
            )

        choice_answer = ChoiceAnswer.objects.create(answer=choice)

        serializer = ChoiceAnswerSerializer(choice_answer)
        return Response({"status": "success", "answer": serializer.data}, status=status.HTTP_201_CREATED)
    
