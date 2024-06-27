from django.shortcuts import render, redirect
from django.http import HttpResponse

import joblib

# Create your views here.

def home(request):
    return render(request, 'base/home.html')


def result(request):

    regressor = joblib.load('insurance_model.sav')
    info_list = []
    context = {}

    if request.method == 'POST':
        user_age= int(request.POST.get('user_age'))
        

        user_sex = request.POST.get('sex')
        user_bmi = float(request.POST.get('bmi'))
        user_children = request.POST.get('children')
        user_smoker = request.POST.get('smoker')
        user_region = request.POST.get('region')


        sex_mapping = {'male': 0, 'female': 1}
        smoker_mapping = {'yes': 0, 'no': 1}
        region_mapping = {'southeast': 0, 'southwest': 1, 'northeast': 2, 'northwest': 3}

        age = int(user_age)
        sex = sex_mapping[user_sex.lower()]
        bmi = float(user_bmi)
        children = int(user_children)
        smoker = smoker_mapping[user_smoker.lower()]
        region = region_mapping[user_region.lower()]

        # Append the features to the list
        info_list.extend([age, sex, bmi, children, smoker, region])

        ins_price = 0
 
        ins_price = regressor.predict([info_list])

        context = {'ins_price':ins_price}
    
    return render(request, 'base/result.html', context)

