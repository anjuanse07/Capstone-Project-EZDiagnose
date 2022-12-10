from django.http import HttpResponse
from django.shortcuts import render

from pathlib import Path
import os

import pandas as pd
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


def index(request):
    return render(request, 'index.html')


def test(request):
    data = pd.read_csv(os.path.join(
        BASE_DIR, 'EZDiagnose/dataset/Training.csv'))
    data = data.drop(columns=['Unnamed: 133'])
    data = data.drop(columns='prognosis')

    arr = []

    for symptom in data:
        arr.append(symptom.replace('_', ' '))
    return render(request, 'test.html', {'data': arr})


def form_diagnose(request):
    data = pd.read_csv(os.path.join(
        BASE_DIR, 'EZDiagnose/dataset/Training.csv'))
    data = data.drop(columns=['Unnamed: 133'])
    data = data.drop(columns='prognosis')

    symptoms = []

    for symptom in data:
        symptoms.append(symptom.replace('_', ' '))
    return render(request, 'form-diagnose.html', {'symptoms': symptoms})


def output_diagnose(request):
    print(request.POST)
    return render(request, 'output-diagnose.html')
