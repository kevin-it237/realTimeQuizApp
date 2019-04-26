def get_results(scores): # Take the score of each players
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
