from django.db import models
from django.contrib.auth.models import User


class Participant(models.Model):
    user = models.OneToOneField(User)
    score = models.IntegerField()


class Question(models.Model):
    question_title = models.CharField(max_length=512)
    question_desc = models.TextField()
    input_data = models.TextField()
    expected_output = models.TextField()


class Submission(models.Model):
    IN_PROGRESS = "IPR"
    RUNTIME_ERROR = "RTE"
    TIMEOUT = "TMO"
    WRONG_ANSWER = "WA"
    ACCEPTED_ANSWER = "AC"

    STATUS_CHOICES = (
        (IN_PROGRESS, "Execution in progress"),
        (RUNTIME_ERROR, "Runtime Error"),
        (TIMEOUT, "Timed out"),
        (WRONG_ANSWER, "Wrong Answer"),
        (ACCEPTED_ANSWER, "Correct Answer")
    )

    LANG_CHOICES = (
        ("PYT", "Python"),
        ("CPP", "C++"),
        ("JAV", "Java"),
        )

    submit_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=3,
                              choices=STATUS_CHOICES,
                              default=IN_PROGRESS)
    program = models.TextField()
    plang = models.CharField(max_length=3,
                             choices=LANG_CHOICES,
                             default="PYT")
    submitter = models.ForeignKey('Participant')
    question_answered = models.ForeignKey('Question')


