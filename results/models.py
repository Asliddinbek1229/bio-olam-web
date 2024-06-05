from django.db import models

# Quiz model        
from quiz_app.models import Quiz

# User model
from users.models import Profile

# Validators
from validators.validators import PERCENTAGE_VALIDATOR


# Result model
class Result(models.Model):
    """
    The results for the quiz answers of a given user
    """ 
    
    date = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True
    )

    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="results_quiz"
    )

    user = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='quiz_profile'
    )

    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=PERCENTAGE_VALIDATOR
    )

    
    def __str__(self):
        return str(self.pk)