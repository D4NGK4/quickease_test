from django.db import models
from summarizer_api.models import UserNotes
from django.utils.translation import gettext_lazy as _ 


# Create your models here.


# User Test Model

class UserTest(models.Model):
    note = models.OneToOneField(UserNotes, on_delete=models.CASCADE, primary_key=True)
    TestScore = models.IntegerField(default=0)
    TestTotalScore = models.IntegerField(default=0)
    TestDateCreated = models.DateTimeField(auto_now_add=True)
    
    class Meta: 
        verbose_name = _("User Test")
        verbose_name_plural = _("User Test")

    def __str__(self):
        return str(self.note)
    
# Test Question Model

class TestQuestion(models.Model):
    test = models.ForeignKey(UserTest, on_delete=models.CASCADE)
    TestQuestion = models.TextField()

    class Meta:
        verbose_name = _("Test Question")
        verbose_name_plural = _("Test Questions")

    def __str__(self):
        return str(self.TestQuestion)
    

# Test Choices Model

class TestChoices(models.Model):
    question = models.ForeignKey(TestQuestion, on_delete=models.CASCADE)
    item_choice_text = models.TextField()
    isAnswer = models.BooleanField()

    class Meta:
        verbose_name = _("Test Choice")
        verbose_name_plural = _("Test Choices")

    def __str__(self):
        return str(self.question) + str(self.isAnswer)
    
# Choice Answer Model
    
class ChoiceAnswer(models.Model):
    answer = models.OneToOneField(TestChoices, on_delete=models.CASCADE, primary_key=True)

    class Meta:
        verbose_name = _("Choice Answer")
        verbose_name_plural = _("Choice Answers")

    def __str__(self):
        return str(self.answer)
