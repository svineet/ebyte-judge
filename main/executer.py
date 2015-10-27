from .models import Submission

import os
import subprocess
import random


def execute(submission):
    if submission.plang=="PYT":
        execute_py(submission)
    elif submission.plang=="JAVA":
        execute_java(submission)
    else:
        execute_cpp(submission)


def execute_py(submission):
    input_ = submission.question_answered.input_data
    expected_out = submission.question_answered.expected_output

    # weird random filename to prevent race conditions and
    # such problems where same file is fought for by
    # two threads
    tmp_prog = "tmp"+str(random.random())+".tmp"
    tmp_file = open(tmp_prog, "w")
    tmp_file.write(submission.program)

    tmp_in = "tmpin"+str(random.random())+".tmpin"
    tmpin = open(tmp_in, "wr")
    tmpin.write(input_)

    tmp_file.close()
    tmpin.close()

    try:
        out = subprocess.check_output(["python", tmp_prog],
            stdin=open(tmp_in), stderr=subprocess.STDOUT)

        if out==expected_out:
            submission.status = Submission.ACCEPTED_ANSWER
            submission.submitter.score += 100
            submission.submitter.save()
            submission.save()
        else:
            submission.status = Submission.WRONG_ANSWER
            submission.save()

        print "input"
        print input_
        print "got: "
        print out
        print "expected: "
        print expected_out
    except subprocess.CalledProcessError:
        submission.status = Submission.RUNTIME_ERROR
        submission.save()


def execute_java(submission):
    pass


def execute_cpp(submission):
    pass
