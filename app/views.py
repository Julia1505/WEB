from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from app.models import *
from app.utilits import *

new_questions = Question.new_questions.all()
hot_questions = Question.hot_questions.all()

def index(request):
    paginator = Paginator(new_questions, 2)
    page_num = request.GET.get('page')
    questions = paginator.get_page(page_num)
    return render(request, "index.html", {"questions":questions,})

def hot(request):
    paginator = Paginator(hot_questions, 2)
    page_num = request.GET.get('page')
    questions = paginator.get_page(page_num)
    return render(request, "hot.html", {"questions":questions})

def question(request, id):
    question = get_object_or_404(Question, pk = id)
    answers = Answer.answers.filter(question = question)

    paginator = Paginator(answers, 2)
    page_num = request.GET.get('page')
    answers = paginator.get_page(page_num)
    return render(request, "question.html", {"question":question, "answers":answers})

def ask(request):
    return render(request, "ask.html", { })

def login(request):
    return render(request, "login.html", {"form_login":form_login })

def signup(request):
    return render(request, "signup.html", {"form_sign_up":form_sign_up })

def tag(request, slug):
    tag_questions = get_object_or_404(Tag.tags.filter(tag=slug)).questions.all()

    paginator = Paginator(tag_questions, 2)
    page_num = request.GET.get('page')
    questions = paginator.get_page(page_num)
    return render(request, "tag.html", {"questions":questions, "slug":slug})

def settings(request):
    return render(request, "settings.html", {"form_settings":form_settings })

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Not found!</h1>')
