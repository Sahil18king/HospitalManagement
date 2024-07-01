from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User

def home(request):
    return render(request, 'index.html')

def signup(request):
    return render(request,'signup.html')

