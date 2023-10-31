from django.shortcuts import render
import openai
from dotenv import load_dotenv
import os
#python manage.py runserver

def home(request):
    return render(request, 'pages/home.html')

def coding(request):
    if request.method == 'POST':
        prompt = request.POST['question']
        language = request.POST['language']
        prompt = "Strictly use the code format, help me to write a " + language + " code according to this demand: \n" + prompt + "[END]"
        load_dotenv()
        openai.api_key = os.environ.get('OPENAI_API_KEY')
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=1024,
        )
        answer = response['choices'][0]['text']
    else:
        answer = None
    return render(request, 'pages/coding.html', {'answer': answer})

def explaining(request):
    if request.method == 'POST':
        prompt = request.POST['question']
        language = request.POST['language']
        prompt = "Explain this " + language + " code with as many details as possible: \n" + prompt + "[END]"
        load_dotenv()
        openai.api_key = os.environ.get('OPENAI_API_KEY')
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=1024,
        )
        answer = response['choices'][0]['text']
    else:
        answer = None
    return render(request, 'pages/explaining.html', {'answer': answer})

def about(request):
    return render(request, 'pages/about.html')