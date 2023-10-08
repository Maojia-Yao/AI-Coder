from django.shortcuts import render
import os

# Create your views here.

def home(request):
    return render(request, 'pages/home.html')

def coding(request):
    return render(request, 'pages/coding.html')

def explaining(request):
    return render(request, 'pages/explaining.html')

def about(request):
    return render(request, 'pages/about.html')