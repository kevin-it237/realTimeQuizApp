from . import models

def calcul_result(user_response, questionId): # user_reponse is an array, questionId a number, return total marks
    # Get true responses in the database
    question = models.Question.objects.get(pk=questionId)
    res = ''
    total_marks = 0
    if ',' in question.reponse_juste: # If there is many true response
        n = len(question.reponse_juste.split(',')) # Number of true resposes

        res = question.reponse_juste.split(',')
        for r in user_response:
            if r in res:
                if n == 2:
                    total_marks += 2.5
                elif n == 3:
                    total_marks += 2
                elif n == 4:
                    total_marks += 1
            else:
                total_marks -= 2

    else: # If there is only one true response
        res = question.reponse_juste
        for r in user_response:
            if r == res:
                total_marks += 5
            else:
                total_marks -= 2           

    return total_marks
    