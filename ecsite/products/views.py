from django.shortcuts import render, redirect
from django.views.generic import View
# from .models import User, Post
from .forms import ChoiceForm, KeywordForm

# Create your views here.

class Top(View):
    def get(self, request):
        return render(request, "main.html")