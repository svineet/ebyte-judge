from .executer import execute
from .forms import SubmissionForm
from .models import Question, Participant, Submission
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth import logout as logout_django
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from threading import Thread


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
            instance.save()

            thr = Thread(target=execute, args=[instance])
            thr.start()

            messages.add_message(request, messages.INFO, 
                "Submission successfully made! Now wait for it to be judged"
                ", keep refreshing the My Submissions page!")
            return HttpResponseRedirect('/main/submissions')
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
        return HttpResponseRedirect('/main/')
    else:
        return render(request, 'main/login.html', {'message': 'invalid login'})


@login_required
def logout(request):
    logout_django(request)
    return HttpResponseRedirect('/main/')


