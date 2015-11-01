from .executer import execute
from .forms import SubmissionForm
from .models import Question, Participant, Submission, Activity
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth import logout as logout_django
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from threading import Thread


SUBMITTED_ACTIVITY_TEXT = "{} submitted a solution for the '{}' question!"


@login_required
def index(request):
    latest_question_list = Question.objects.all()
    context = {'questions': latest_question_list}
    return render(request, 'main/index.html', context)


@login_required
def detail(request, question_id):
    q = get_object_or_404(Question, pk=question_id)
    return render(request, 'main/detail.html', {'question': q})


@login_required
def submit(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if 'program' in request.POST:
        form = SubmissionForm(request.POST)
        if form.is_valid():
            instance = Submission()
            instance.program = request.POST['program']
            instance.plang = request.POST['plang']
            instance.submitter = request.user.participant
            instance.question_answered = question

            row = Submission.objects.filter(question_answered=question,
                                            submitter=instance.submitter,
                                            status=instance.ACCEPTED_ANSWER)
            if row:
                messages.add_message(request, messages.INFO,
                    "You cannot re-submit a solved question.")
                return redirect('index')

            instance.save()

            act = Activity()
            act.text = SUBMITTED_ACTIVITY_TEXT.format(
                request.user.username, question.question_title)
            act.act_type = "INF"
            act.save()

            thr = Thread(target=execute, args=[instance])
            thr.start()

            messages.add_message(request, messages.INFO, 
                "Submission successfully made! Now wait for it to be judged"
                ", keep refreshing the My Submissions page!")
            return redirect('list_submissions')
        else:
            return render(request, 'main/submit.html', 
                {
                    'errors': form.errors
                })
    else:
        return render(request, 'main/submit.html',
            {
                'question': question
            })


@login_required
def leaderboard(request):
    users = Participant.objects.order_by('-score')
    return render(request, 'main/leaderboard.html', 
        {'participants': users})


@login_required
def list_submissions(request):
    subms = Submission.objects\
        .filter(submitter_id=request.user.participant.id)\
        .order_by('-submit_time');

    return render(request, 'main/list_submissions.html',
        {
            'submissions': subms
        })



def login(request):
    if 'username' not in request.POST:
        return render(request, 'main/login.html', {})

    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(username=username, password=password)
    if user is not None:
        login_django(request, user)
        return redirect('index')
    else:
        return render(request, 'main/login.html', {'message': 'invalid login'})


@login_required
def logout(request):
    logout_django(request)
    return redirect('index')


# No login required for activity feed so that we can 
# access it without making an account
# todo: paginate
def list_activity(request):
    activities = Activity.objects.order_by('-time')[:10]
    return render(request, 'main/activity_list.html', 
        {
            'activity_list': activities
        })

