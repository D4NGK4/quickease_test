from django.db import models
from users.models import User

class Badge(models.Model):
    badge_name = models.CharField(max_length=30, unique=True)  # Ensure badge names are unique
    badge_description = models.CharField(max_length=150)

    class Meta: 
        verbose_name = "Badge"
        verbose_name_plural = "Badges"
    
    def __str__(self):
        return self.badge_name


class Achievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')  # Add related_name for better access
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='achievements')  # Add related_name for better access
    date_achieved = models.DateTimeField(auto_now_add=True)

    class Meta: 
        verbose_name = "Achievement"
        verbose_name_plural = "Achievements"
        unique_together = ('user', 'badge')  # Enforce unique user-badge pair

    def __str__(self):
        return f"{self.badge} | {self.user}"

# Create your models here.
