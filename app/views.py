from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from app.models import *

# <span class="badge bg-dark">hot</span>
#                             <span class="badge bg-danger">crazy</span>
#                             <span class="badge bg-primary">auf</span>


tags = Tag.tags.all()
new_questions = Question.new_questions.all()
hot_questions = Question.hot_questions.order_by('rating')
# answers = Answer.answers.all()
users = User.users.all()


def index(request):
    paginator = Paginator(new_questions, 2)
    page_num = request.GET.get('page')
    questions = paginator.get_page(page_num)
    return render(request, "index.html", {"questions":questions,})

def hot(request):
    paginator = Paginator(hot_questions, 2)
    page_num = request.GET.get('page')
    questions = paginator.get_page(page_num)
    return render(request, "hot.html", {  "tags":tags, "questions":questions, })

def question(request, id):
    # question = Question.new_questions.get(pk=id)
    question = get_object_or_404(Question, pk = id)
    answers = Answer.answers.filter(question = question)

    paginator = Paginator(answers, 2)
    page_num = request.GET.get('page')
    answers = paginator.get_page(page_num)
    return render(request, "question.html", {  "question":question, "answers":answers})


def ask(request):
    return render(request, "ask.html", { })

def login(request):
    return render(request, "login.html", { })

def signup(request):
    return render(request, "signup.html", { })

def tag(request, tag):
    # tag_question = Question.new_questions.filter(tag=tag)
    tag_question = get_object_or_404(Question.new_questions.filter(tag = tag))
    if len(tag_question) == 0:
        raise pageNotFound

    paginator = Paginator(tag_question, 2)
    page_num = request.GET.get('page')
    questions = paginator.get_page(page_num)

    return render(request, "tag.html", {"questions":question})

def settings(request):
    return render(request, "settings.html", { })


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Not found!</h1>')

