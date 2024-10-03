from django.db import models
from django.utils.translation import gettext_lazy as _ 
from .text_summarizer import summarize
from users.models import User
from .title_generator import generate_title
from django.db import transaction

# Create your models here.

class UserNotes(models.Model):
    notetitle = models.TextField(_("Note Title"), default="")
    notecontents = models.TextField(_("Note Contents"))
    notedatecreated = models.DateTimeField(auto_now_add=True)
    notesummary = models.TextField(_("Note Summary"), blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    
    class Meta: 
        verbose_name = _("User Note")
        verbose_name_plural = _("User Notes")
    
    def save(self, *args, **kwargs):
        with transaction.atomic():
            if not self.notesummary:  
                self.notesummary = summarize(
                    text=self.notecontents,
                    detail=0.75, 
                    model='gpt-4o-mini',
                    additional_instructions='''You are a professional tutor and you are reading the provided material to generate comprehensive summary notes for my upcoming test.

                                            Generate a summary notes that is clear, concise, and easy to understand.

                                            Respond in html format only use ordered list, headings, and unordered list. Remove extras like ``` or the tag/word html and do not use markdowns elements. You may also read inline LaTex and block LaTex formulas

                                            The summary notes should contain overview summary (a brief, high-level overview of the main topic covered in the material. Focus on summarizing the core ideas and key concepts in 2-3 sentences), and Detailed Breakdown with Key Points (Break the topic into logical sections or themes. For each section, list the key points or takeaways in a bulleted or numbered format for easy reading). Use h2 as section headers for Overview Summary and Key Points.
                                            ''',
                    summarize_recursively=True
                )
                self.notetitle = generate_title(self.notesummary)
            super(UserNotes, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.notetitle