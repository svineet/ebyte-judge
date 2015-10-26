from .models import Submission


def execute(submission):
    submission.status = Submission.ACCEPTED_ANSWER
    submission.submitter.score += 100
    submission.submitter.save()
    submission.save()
