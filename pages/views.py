from django.shortcuts import render, redirect
import openai
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import RequestAndAnswer
from .forms import CustomUserCreationForm


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')  # Redirect to login page
        else:
            if 'password2' in form.errors:  # Check for password errors
                password_errors = form.errors['password2']
                error_msg = None
                if "The password is too similar to the username." in password_errors:
                    error_msg = 'The password is too similar to the username.'
                elif "This password is too short. It must contain at least 8 characters." in password_errors:
                    error_msg = 'The password is too short. It must contain at least 8 characters.'
                elif "The two password fields didn’t match." in password_errors:
                    error_msg = 'The entered passwords are inconsistent, please try again.'

                if error_msg:
                    messages.error(request, error_msg)
            else:
                messages.error(request, 'Registration failed, please check your input and try again.')  # Other error messages
            return render(request, 'pages/register.html', {'form': form})
    else:
        form = CustomUserCreationForm()
    return render(request, 'pages/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password. Please try again.")
                return render(request, 'pages/login.html', {'form': form})
        else:
            # Check for specific form errors
            if 'username' in form.errors:
                for error in form.errors['username']:
                    messages.error(request, error)
            elif 'password' in form.errors:
                for error in form.errors['password']:
                    messages.error(request, error)
            elif '__all__' in form.errors:
                for error in form.errors['__all__']:
                    messages.error(request, error)
            else:
                messages.error(request, 'There was an error with your submission. Please check your input.')
            
            return render(request, 'pages/login.html', {'form': form})
    else:
        form = AuthenticationForm()
    return render(request, 'pages/login.html', {'form': form})


@login_required
def profile(request):
    username = request.user.username
    user = User.objects.get(username=username)
    request_and_answer = RequestAndAnswer.objects.filter(username=username)

    context = {
        'user': user,
        'request_and_answer': request_and_answer,
    }

    return render(request, 'pages/profile.html', context)


def home(request):
    return render(request, 'pages/home.html')


def about(request):
    return render(request, 'pages/about.html')


@login_required
def coding(request):
    answer = generate_answer(request, 'coding')
    request_text = request.POST.get('question', '')
    
    if answer is not None:
        username = request.user.username
        # Create a RequestAndAnswer object and store the request and answer text
        request_and_answer = RequestAndAnswer(request=request_text, answer=answer, username=username)
        request_and_answer.save()

    return render(request, 'pages/coding.html', {'answer': answer})

@login_required
def explaining(request):
    answer = generate_answer(request, 'explaining')
    request_text = request.POST.get('question', '')

    if answer is not None:
        username = request.user.username
        # Create a RequestAndAnswer object and store the request and answer text
        request_and_answer = RequestAndAnswer(request=request_text, answer=answer, username=username)
        request_and_answer.save()

    return render(request, 'pages/explaining.html', {'answer': answer})

@login_required
def evaluation(request):
    answer = generate_answer(request, 'evaluation')
    request_text = request.POST.get('question', '')

    if answer is not None:
        username = request.user.username
        # Create a RequestAndAnswer object and store the request and answer text
        request_and_answer = RequestAndAnswer(request=request_text, answer=answer, username=username)
        request_and_answer.save()
        
    return render(request, 'pages/evaluation.html', {'answer': answer})


def generate_answer(request, task):
    if check(request.method):
        prompt = request.POST['question']
        language = request.POST['language']
        prompt = get_prompt(task, prompt, language)

        # Use the API key from Django settings
        openai.api_key = settings.OPENAI_API_KEY
        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                max_tokens=1024,
            )
            answer = response['choices'][0]['text']
        except openai.error.OpenAIError as e:
            # Handle OpenAI errors
            answer = f"An error occurred: {str(e)}"
        except Exception as e:
            # Handle other errors
            answer = f"An unexpected error occurred: {str(e)}"
    else:
        answer = None
    return answer


def check(method):
    return method == 'POST'


def get_prompt(task, prompt, language):
    if task == 'coding':
        return f"Write a {language} code for the following requirement: \n{prompt}\n[END]"
    elif task == 'explaining':
        return f"Provide a detailed explanation for this {language} code: \n{prompt}\n[END]"
    elif task == 'evaluation':
        return f"Review and assess this {language} code: \n{prompt}\n[END]"

    else:
        return prompt
