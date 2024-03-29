#Quiz model

from django.db import models

from django.contrib.auth import get_user_model
User = get_user_model()

class Question(models.Model):
    libelle = models.CharField(max_length=255, unique=True)
    reponse_juste = models.CharField(max_length=255)
    users = models.ManyToManyField(User, through='UserQuestion')

    def __str__(self):
        return self.libelle

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class UserQuestion(models.Model):
    user = models.ForeignKey(User, related_name='user_questions', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='memberships', on_delete=models.CASCADE)
    reponse = models.CharField(max_length=255)
    point_obtenu = models.FloatField() 

    def __str__(self):
        return self.user.username

    class Meta():
        unique_together = ('question', 'user')


class Response(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    libelle = models.CharField(max_length=255)

    def __str__(self):
        return self.libelle

class QuizControl(models.Model):
    is_stopped = models.BooleanField(default=False)

    def __str__(self):
        return str(self.is_stopped)