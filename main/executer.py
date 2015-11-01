from .models import Submission

import os
import subprocess
import random
import re


def execute(submission):
    if submission.plang=="PYT":
        execute_py(submission)
    elif submission.plang=="JAV":
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
    tmp_file.close()

    tmp_in = "tmpin"+str(random.random())+".tmpin"
    tmpin = open(tmp_in, "wr")
    tmpin.write(input_)
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
    except subprocess.CalledProcessError as e:
        print e.output
        submission.status = Submission.RUNTIME_ERROR
        submission.save()

    try:
        os.remove(tmp_prog)
        os.remove(tmp_in)
    except:
        pass


def execute_java(submission):
    input_ = submission.question_answered.input_data
    expected_out = submission.question_answered.expected_output
    # expected_out = expected_out.replace('\r\n', '\n')

    for i in re.split('\nclass ', submission.program)[1:]:
        if re.search('\n\s*public static void main', i):
            class_name = re.search('(\w*)', i).group(1)

    tmp_prog = class_name+".java"
    tmp_file = open(tmp_prog, "w")
    tmp_file.write(submission.program)
    tmp_file.close()


    tmp_in = "tmpin"+str(random.random())+".tmpin"
    tmpin = open(tmp_in, "wr")
    tmpin.write(input_)
    tmpin.close()

    try:
        subprocess.check_call(["javac", tmp_prog])
        out = subprocess.check_output(["java", class_name],
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
    except subprocess.CalledProcessError as e:
        print e.output
        submission.status = Submission.RUNTIME_ERROR
        submission.save()

    try:
        os.remove(tmp_prog)
        os.remove(tmp_in)
        os.remove(class_name+".class")
    except:
        pass

def execute_cpp(submission):
    input_ = submission.question_answered.input_data
    expected_out = submission.question_answered.expected_output

    # weird random filename to prevent race conditions and
    # such problems where same file is fought for by
    # two threads
    tmp_prog = "tmp"+str(random.random())+".cpp"
    tmp_file = open(tmp_prog, "w")
    tmp_file.write(submission.program)
    tmp_file.close()

    tmp_in = "tmpin"+str(random.random())+".tmpin"
    tmpin = open(tmp_in, "wr")
    tmpin.write(input_)
    tmpin.close()

    try:
        # This is very platform/compiler specific stuff.
        if os.uname()[0] == 'Linux':
            subprocess.check_call(["c++", tmp_prog])
            out = subprocess.check_output(["./a.out"],
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
    except subprocess.CalledProcessError as e:
        print e.output
        submission.status = Submission.RUNTIME_ERROR
        submission.save()

    try:
        os.remove(tmp_prog)
        os.remove(tmp_in)
        os.remove("a.out")
    except:
        pass
