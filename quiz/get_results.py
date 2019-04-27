from django.contrib.auth import get_user_model
User = get_user_model()

from django.db.models import Sum, Count

from . import models

def get_results(): # return ordered results
    # Recuperer les resultats
    scores = models.UserQuestion.objects.all().values('user').distinct().annotate(score = Sum('point_obtenu'), n = Count('user') * 10, questions = Count('user') * 10).order_by('-score')
    final_results = []
    # For Each score I find the correspondant user
    i = 1 # Le rang
    for el in scores:
        user = User.objects.get(pk=el['user'])
        user_dict = {'username': user.username, 'email': user.email, 'name': user.first_name}
        el = {**el}
        el['n'] = i
        i = i + 1
        result = {**el, **user_dict}
        final_results.append(result)
    return final_results
