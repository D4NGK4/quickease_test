from rest_framework import serializers
from .models import UserTest, TestQuestion, TestChoices, ChoiceAnswer

class UserTestSerializer(serializers.ModelSerializer):
    note = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = UserTest
        fields = "__all__"

class TestQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestQuestion
        fields = ['id', 'TestQuestion']
        read_only_fields = ['id']
        
class TestChoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestChoices
        fields = ['id', 'item_choice_text', 'isAnswer']
        read_only_fields = ['id']
        
class ChoiceAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChoiceAnswer
        fields = ['answer']
        read_only_fields = ['answer']
        
        
