from .models import Submission, Activity
from judge import settings

import os
import subprocess
import random
import re


CORRECT_SUBMISSION_TEXT = "{} got the {} question right! +{} to them!"
WRONG_SUBMISSION_TEXT = "{} got the {} question wrong! Better luck next time!"
RTE_SUBMISSION_TEXT = "{} got a Runtime Error in the {} question! Better luck next time!"
TME_SUBMISSION_TEXT =  "{} got a Timeout in the {} question! Try harder!"


def execute(submission):
    if submission.plang=="PYT":
        execute_py(submission)
    elif submission.plang=="JAV":
        execute_java(submission)
    else:
        execute_cpp(submission)


def execute_py(submission):
    input_ = submission.question_answered.input_data.replace('\r', '')
    expected_out = submission.question_answered.expected_output.replace('\r', '')

    # weird random filename to prevent race conditions and
    # such problems where same file is fought for by
    # two threads
    tmp_prog = "tmp"+str(random.random())+".tmp"
    tmp_file = open(tmp_prog, "w")
    tmp_file.write(submission.program)
    tmp_file.close()

    tmp_in = "tmpin"+str(random.random())+".tmpin"
    tmpin = open(tmp_in, "w")
    tmpin.write(input_)
    tmpin.close()

    try:
        out = subprocess.check_output(["python", tmp_prog],
                stdin=open(tmp_in), stderr=subprocess.STDOUT,
                timeout=5)
        out = out.decode("ascii").strip()

        if out.strip()==expected_out.strip():
            submission.status = Submission.ACCEPTED_ANSWER
            time_diff = settings.END_TIME - submission.submit_time
            submission.submitter.score += 100 + (time_diff.seconds/60)
            submission.submitter.save()
            submission.save()

            act = Activity()
            act.text = CORRECT_SUBMISSION_TEXT.format(
                submission.submitter.user.username, submission.question_answered.question_title, 
                submission.submitter.score)
            act.act_type = "SUC"
            act.save()
        else:
            submission.status = Submission.WRONG_ANSWER
            submission.save()

            act = Activity()
            act.text = WRONG_SUBMISSION_TEXT.format(
                submission.submitter.user.username, submission.question_answered.question_title)
            act.act_type = "FAL"
            act.save()

        from pprint import pprint
        pprint ("input")  
        pprint (input_)
        pprint ("got: ")
        pprint (out)
        pprint("expected: ")
        pprint (expected_out)
    except subprocess.CalledProcessError as e:
        print (e.output)
        submission.status = Submission.RUNTIME_ERROR
        submission.save()

        act = Activity()
        act.text = RTE_SUBMISSION_TEXT.format(
            submission.submitter.user.username, submission.question_answered.question_title)
        act.act_type = "FAL"
        act.save()
    except subprocess.TimeoutExpired as e:
        submission.status = Submission.TIMEOUT
        submission.save()

        act = Activity()
        act.text = TME_SUBMISSION_TEXT.format(
            submission.submitter.user.username, submission.question_answered.question_title)
        act.act_type = "FAL"
        act.save()

    try:
        os.remove(tmp_prog)
        os.remove(tmp_in)
    except:
        pass


def execute_java(submission):
    input_ = submission.question_answered.input_data
    expected_out = submission.question_answered.expected_output.replace('\r\n', '\n').strip()

    for i in re.split('class ', submission.program)[1:]:
        if re.search('\n\s*public static void main', i):
            class_name = re.search('(\w*)', i).group(1)

    tmp_prog = class_name+".java"
    tmp_file = open(tmp_prog, "w")
    tmp_file.write(submission.program)
    tmp_file.close()


    tmp_in = "tmpin"+str(random.random())+".tmpin"
    tmpin = open(tmp_in, "w")
    tmpin.write(input_)
    tmpin.close()

    try:
        subprocess.check_call(["javac", tmp_prog])
        out = subprocess.check_output(["java", class_name],
            stdin=open(tmp_in), stderr=subprocess.STDOUT,
            timeout=5)
        out = out.decode("ascii").strip()

        if out==expected_out:
            submission.status = Submission.ACCEPTED_ANSWER
            time_diff = settings.END_TIME - submission.submit_time
            submission.submitter.score += 100 + (time_diff.seconds/60)
            submission.submitter.save()
            submission.save()

            act = Activity()
            act.text = CORRECT_SUBMISSION_TEXT.format(
                submission.submitter.user.username, submission.question_answered.question_title,
                submission.submitter.score)
            act.act_type = "SUC"
            act.save()
        else:
            submission.status = Submission.WRONG_ANSWER
            submission.save()

            act = Activity()
            act.text = WRONG_SUBMISSION_TEXT.format(
                submission.submitter.user.username, submission.question_answered.question_title)
            act.act_type = "FAL"
            act.save()

        from pprint import pprint
        print ("input"   )
        pprint (input_)
        print ("got: ")
        pprint (out)
        print ("expected: ")
        pprint (expected_out)
    except subprocess.CalledProcessError as e:
        print (e.output)
        submission.status = Submission.RUNTIME_ERROR
        submission.save()

        act = Activity()
        act.text = RTE_SUBMISSION_TEXT.format(
            submission.submitter.user.username, submission.question_answered.question_title)
        act.act_type = "FAL"
        act.save()
    except subprocess.TimeoutExpired as e:
        submission.status = Submission.TIMEOUT
        submission.save()

        act = Activity()
        act.text = TME_SUBMISSION_TEXT.format(
            submission.submitter.user.username, submission.question_answered.question_title)
        act.act_type = "FAL"
        act.save()

    try:
        os.remove(tmp_prog)
        os.remove(tmp_in)
        os.remove(class_name+".class")
    except:
        pass

def execute_cpp(submission):
    input_ = submission.question_answered.input_data
    expected_out = submission.question_answered.expected_output
    expected_out = expected_out.replace('\r\n', '\n').replace('\r', '\n').strip()

    # weird random filename to prevent race conditions and
    # such problems where same file is fought for by
    # two threads
    tmp_prog = "tmp"+str(random.random())+".cpp"
    tmp_file = open(tmp_prog, "w")
    tmp_file.write(submission.program)
    tmp_file.close()

    tmp_in = "tmpin"+str(random.random())+".tmpin"
    tmpin = open(tmp_in, "w")
    tmpin.write(input_)
    tmpin.close()

    output_filename = str(random.random())+".out"

    try:
        # This is very platform/compiler specific stuff.
        if os.uname()[0] == 'Linux':
            subprocess.check_call(["c++", "-o", output_filename, tmp_prog])
            out = subprocess.check_output(["./"+output_filename],
                stdin=open(tmp_in), stderr=subprocess.STDOUT,
                timeout=5)
            out = out.decode("ascii").strip()

        if out==expected_out:
            submission.status = Submission.ACCEPTED_ANSWER
            time_diff = settings.END_TIME - submission.submit_time
            submission.submitter.score += 100 + (time_diff.seconds/60)
            submission.submitter.save()
            submission.save()

            act = Activity()
            act.text = CORRECT_SUBMISSION_TEXT.format(
                submission.submitter.user.username, submission.question_answered.question_title,
                submission.submitter.score)
            act.act_type = "SUC"
            act.save()
        else:
            submission.status = Submission.WRONG_ANSWER
            submission.save()

            act = Activity()
            act.text = WRONG_SUBMISSION_TEXT.format(
                submission.submitter.user.username, submission.question_answered.question_title)
            act.act_type = "FAL"
            act.save()

        from pprint import pprint
        print ("input"   )
        pprint (input_)
        print ("got: ")
        pprint (out)
        print ("expected: ")
        pprint (expected_out)
    except subprocess.CalledProcessError as e:
        print (e.output)
        submission.status = Submission.RUNTIME_ERROR
        submission.save()

        act = Activity()
        act.text = RTE_SUBMISSION_TEXT.format(
            submission.submitter.user.username, submission.question_answered.question_title)
        act.act_type = "FAL"
        act.save()
    except subprocess.TimeoutExpired as e:
        submission.status = Submission.TIMEOUT
        submission.save()

        act = Activity()
        act.text = TME_SUBMISSION_TEXT.format(
            submission.submitter.user.username, submission.question_answered.question_title)
        act.act_type = "FAL"
        act.save()

    try:
        os.remove(tmp_prog)
        os.remove(tmp_in)
        os.remove(output_filename)
    except:
        pass
