from django.contrib import auth
from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from app.forms import *
from app.models import *
from app.utilits import *

new_questions = Question.new_questions.all()



def paginate(content, request, number):
    paginator = Paginator(content, number)
    page_num = request
    return paginator.get_page(page_num)


def index(request):
    questions = paginate(new_questions, request.GET.get('page'), 20)
    return render(request, "index.html", {"questions":questions})

def hot(request):
    hot_questions = Question.hot_questions.all()
    questions = paginate(hot_questions, request.GET.get('page'), 20)
    return render(request, "hot.html", {"questions":questions})

def question(request, id):
    question = get_object_or_404(Question, pk = id)
    answers = Answer.answers.filter(question = question)

    answers = paginate(answers, request.GET.get('page'), 10)
    return render(request, "question.html", {"question":question, "answers":answers})

def ask(request):
    return render(request, "ask.html", { })

def login(request):
    print(request.POST)
    if request.method == 'GET':
        form = LoginForm()
    elif request.method == 'POST':
        user_form = LoginForm(data = request.POST)
        if user_form.is_valid():
            user = auth.authenticate(request, **user_form.cleaned_data)
            if user:
                return redirect(reverse('home'))

    return render(request, "login.html", {"form_login":form_login, "form":form })

def signup(request):
    return render(request, "signup.html", {"form_sign_up":form_sign_up })

def tag(request, slug):
    tag_questions = get_object_or_404(Tag.tags.filter(tag=slug)).questions.all()

    questions = paginate(tag_questions, request.GET.get('page'), 20)
    return render(request, "tag.html", {"questions":questions, "slug":slug})

def settings(request):
    return render(request, "settings.html", {"form_settings":form_settings })

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Not found!</h1>')
