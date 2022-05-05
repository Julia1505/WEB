from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from  haystack.query import SearchQuerySet

from app.forms import *
from app.models import *
from app.utilits import *


def paginate(content, request, number):
    paginator = Paginator(content, number)
    page_num = request
    return paginator.get_page(page_num)

def search(query, request, search_field):
    search_query = request.GET.get('search','')
    if search_query:
        if search_field == 'title':
            return query.filter(title__icontains=search_query).all()
        elif search_field == 'content':
            return query.filter(content__icontains=search_query).all()
    else:
        return query.all()

def index(request):
    new_questions = search(Question.new_questions, request, 'title')
    questions = paginate(new_questions, request.GET.get('page'), 20)
    return render(request, "index.html", {"questions":questions})

def hot(request):
    hot_questions = search(Question.hot_questions, request, 'title')
    questions = paginate(hot_questions, request.GET.get('page'), 20)
    return render(request, "hot.html", {"questions":questions})

def question(request, id):

    if request.method == 'POST':
        form = AnswerForm(request.user, id, data=request.POST)
        print(id,  request.POST, 'ggg')
        if form.is_valid():
            quest = form.save().question
            url = quest
            return redirect(url)
    else:
        form = AnswerForm(request.user, id)
    print(id, request.POST, 'ggg')

    question = get_object_or_404(Question, pk = id)

    answers = Answer.answers.filter(question = question)
    answers = search(answers, request, 'content')

    answers = paginate(answers, request.GET.get('page'), 10)
    return render(request, "question.html", {"question":question, "answers":answers, "form":form,})



@login_required
def ask(request):
    if request.method == 'POST':
        form = QuestionForm(request.user, data=request.POST)
        if form.is_valid():
            question = form.save()  #?
            url = question.get_absolute_url()
            return redirect(url)
    else:
        form = QuestionForm(request.user, data=request.POST)
    return render(request, "ask.html", {'form':form, })

def login(request):
    # print(request.POST)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user:
                print(user)
                return redirect(reverse('home'))
            else:
                return HttpResponse('Bad auth')
    else:
        form = LoginForm()

    return render(request, "login.html", { "form":form })

@login_required()
def logout(request):
    logout(request)
    return redirect(reverse('login'))

def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()

            login(request)   # чет не так
            return redirect(reverse('home'))


    elif request.method == 'GET':
        form = RegisterForm()
    return render(request, 'signup.html', {'form':form})



def tag(request, slug):
    tag_questions = get_object_or_404(Tag.tags.filter(tag=slug)).questions.all()

    questions = paginate(tag_questions, request.GET.get('page'), 20)
    return render(request, "tag.html", {"questions":questions, "slug":slug})

@login_required
def settings(request):
    return render(request, "settings.html", {"form_settings":form_settings })

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Not found!</h1>')


