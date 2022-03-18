from re import template
from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate,logout
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.views.generic.list import ListView
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required

# Create your views here.

class LoginView(LoginView):
    template_name = None

