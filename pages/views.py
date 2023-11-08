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


# Handle the registration of new users
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login') # Redirect to login page after successful registration
        else:
            # Initialize an empty list to collect error messages
            error_messages = []

            # Check for specific password errors and add them to the list
            password_errors = form.errors.get('password2', [])
            for error in password_errors:
                if "The password is too similar to the username." in error:
                    error_messages.append('The password is too similar to the username.')
                if "This password is too short. It must contain at least 8 characters." in error:
                    error_messages.append('The password is too short. It must contain at least 8 characters.')
                if "The two password fields didn’t match." in error:
                    error_messages.append('The entered passwords do not match, please try again.')

            # If there are any collected error messages, add them as a single message
            if error_messages:
                messages.error(request, " ".join(error_messages))
            else:
                # For other errors that may not be related to password2
                messages.error(request, 'Registration failed, please check your input and try again.')

            return render(request, 'pages/register.html', {'form': form})
    else:
        form = CustomUserCreationForm()
    return render(request, 'pages/register.html', {'form': form})


# Handle the login functionality
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home') # Redirect to home page after successful login
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


# Display user profile
@login_required  # Require user to be logged in to view this page
def profile(request):
    username = request.user.username
    user = User.objects.get(username=username)
    request_and_answer = RequestAndAnswer.objects.filter(username=username)

    context = {
        'user': user,
        'request_and_answer': request_and_answer,
    }

    return render(request, 'pages/profile.html', context)


# Render the home page
def home(request):
    return render(request, 'pages/home.html')


# Render the about page
def about(request):
    return render(request, 'pages/about.html')


# Handle the coding question-answering functionality
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


# Similar to the coding view, but for explaining code
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


# Similar to the above views but for evaluating code
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


# Generate an answer to the user's question using OpenAI API
def generate_answer(request, task):
    if check(request.method):  # Check if request method is POST
        # Retrieve the user's question and the programming language from the POST data
        prompt = request.POST['question']
        language = request.POST['language']

        # Format the prompt based on the type of task
        prompt = get_prompt(task, prompt, language)

        # Use the OpenAI API key from Django settings
        openai.api_key = settings.OPENAI_API_KEY
        try:
            # Make an API call to OpenAI's Completion endpoint with the specified parameters
            response = openai.Completion.create(
                model="text-davinci-003",  # Specify the model to use
                prompt=prompt,             # Provide the formatted prompt
                max_tokens=1024,           # Limit the number of tokens in the response, including words and pieces of words
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


# Helper function to check if the request method is POST
def check(method):
    return method == 'POST'


# Constructs the appropriate prompt for the given task
def get_prompt(task, prompt, language):
    if task == 'coding':
        return f"Write a {language} code for the following requirement: \n{prompt}\n[END]"
    elif task == 'explaining':
        return f"Provide a detailed explanation for this {language} code: \n{prompt}\n[END]"
    elif task == 'evaluation':
        return f"Review and assess this {language} code: \n{prompt}\n[END]"

    else:
        return prompt
