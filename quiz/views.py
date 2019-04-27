#View for posts
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.core import serializers

from random import randint
import json
from django.http import JsonResponse, HttpResponse

from . import models
from . import forms

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from .verify_result import calcul_result
from .get_results import get_results

User = get_user_model()

N = 5 # Number of question to answer

# Create your views here.

@login_required(login_url='/account/login/')
def index(request):
    # Verify is quiz is not stop by the admin
    is_stopped = models.QuizControl.objects.get(pk=1)
    if is_stopped.is_stopped: # If quiz is stopped
        n = models.UserQuestion.objects.all().count()
        # If nobody have'nt already answerd
        if n == 0: 
            return render(request, 'quiz/waiting.html')
        else: # The admin have stopped the quiz, redirect to thank you page
            score = models.UserQuestion.objects.filter(user=request.user).aggregate(Sum('point_obtenu'))
            ctx = {'total': score}
            if score.get('point_obtenu__sum') == None:
                ctx = {'total': {'score': 0 }}
            return render(request, 'quiz/thankyou.html', context=ctx)

    # When user validate a question
    if request.method == 'POST':
        # Get the user input
        user_response = json.loads(request.body.decode('utf-8'))
        # Get the user responses in string form
        questionId = user_response['questionId']
        response_data = ''
        if len(user_response['response']) != 0:
            if len(user_response['response']) == 1:
                response_data = user_response['response'][0]
            else:
                response_data = ','.join(user_response['response'])
        # Save user input in the database
        total_marks = calcul_result(user_response['response'], questionId)
        question = models.Question.objects.get(pk=questionId)
        data = models.UserQuestion(user=request.user, question=question, reponse=response_data, point_obtenu=total_marks)
        data.save()
        #return JsonResponse(status = 401 , data = {'success' : '/quiz/' })
        return HttpResponse(status=201)
    # Generate a question
    else:
        # Get all questions
        questions = models.Question.objects.all()
        # Get the total number of question in the db
        NUM_QUESTIONS = questions.count()
        # Find questions already anwsered
        already_anwsered = models.UserQuestion.objects.filter(user=request.user)
        # Number of already anwsered
        num_already_anwsered = already_anwsered.count()

        # Ids of All questions
        ids = [question.id for question in questions]
        # Ids of Already anwsered
        already_anwsered_ids = [question.question_id for question in already_anwsered]
        print(already_anwsered_ids)

        # Find if he have not anwserd all his questions
        if (num_already_anwsered < N ):
            # Find a random question
            random_question_id = randint(1, NUM_QUESTIONS)
            # If the question is allready answered
            while random_question_id in already_anwsered_ids:
                print(random_question_id)
                # Generate a new random
                random_question_id = randint(1, NUM_QUESTIONS)

            # Get this question
            question = models.Question.objects.get(pk=random_question_id)
            # Get correspondant responses
            responses = models.Response.objects.filter(question__pk=random_question_id)
        elif (num_already_anwsered == N ): # Il a terminé le jeux
            # Calculer son score
            score = models.UserQuestion.objects.filter(user=request.user).aggregate(Sum('point_obtenu'))
            ctx = {'total': score}
            return render(request, 'quiz/thankyou.html', context=ctx)

        # Display
        ctx = {'question': question, 'responses': responses, 'n': num_already_anwsered + 1}
        #print(str(questions.query))  
    return render(request, 'quiz/quiz.html', context = ctx)


def dashboard(request):
    final_results = get_results()
    if request.user.username == 'inchtechs':
        is_stopped = models.QuizControl.objects.get(pk=1) # Find if quiz is already stopped
        if request.method == 'POST':
            return JsonResponse({'data': final_results, 'is_stopped': is_stopped.is_stopped})
        else:
            ctx = {'scores': final_results, 'number_of_questions': N, 'is_stopped': is_stopped.is_stopped}
            return render(request, 'quiz/dashboard.html', context = ctx)
    else:
        return redirect('quiz:home')   

# Stop the quiz
def stop_quiz(request):
    if request.method == 'POST':
        # Load Post data from API
        changed = json.loads(request.body.decode('utf-8'))
        # Get the user responses in string form
        new_value = changed['haveStopped']
        # Update the continued field in db
        models.QuizControl.objects.filter(pk=1).update(is_stopped = new_value)
        print(new_value)
        return HttpResponse(new_value)
    else:
        return HttpResponse(0)

# Check when redirect
def check_when_redirect(request):
    print(request.method)
    if request.method == 'POST':
        # get the status to the db
        is_stopped = models.QuizControl.objects.get(pk=1) # Find if quiz is already stopped
        return HttpResponse(is_stopped.is_stopped)
    else:
        return redirect('quiz:home')
