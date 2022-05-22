import json

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.forms import model_to_dict
from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_http_methods, require_POST

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
        if form.is_valid():
            quest = form.save().question
            url = quest
            return redirect(url)
    else:
        form = AnswerForm(request.user, id)

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
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user:
                print(user)
                auth.login(request, user)

                return redirect(reverse('home'))
            else:
                form.add_error(None, 'Incorrect login or password')
    else:
        form = LoginForm()

    return render(request, "login.html", { "form":form })

@login_required()
def logout(request):
    auth.logout(request)
    return redirect(reverse('login'))

def signup(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, request.FILES)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()

            new_profile = Profile.users.create(user=new_user)
            new_profile.avatar = user_form.cleaned_data['avatar']
            new_profile.save()
            auth.login(request, new_user)
            return redirect(reverse('home'))
        else:

            print("bad")

    else:
        user_form = UserForm()
    return render(request, 'signup.html', {'user_form':user_form})



def tag(request, slug):
    tag_questions = get_object_or_404(Tag.tags.filter(tag=slug)).questions.all()

    questions = paginate(tag_questions, request.GET.get('page'), 20)
    return render(request, "tag.html", {"questions":questions, "slug":slug})

@login_required
@require_http_methods(['GET','POST'])
def settings(request):
    if request.method == 'POST':
        initial_data = request.POST
        instance = request.user
        user_form = SettingsForm(initial=initial_data, instance = instance, files = request.FILES)
        if user_form.is_valid():
            user_form.save()

            return redirect(reverse('home'))
    else:
        initial_data = model_to_dict(request.user)
        initial_data['avatar'] = request.user.profile.avatar
        user_form = SettingsForm(initial=initial_data)


    return render(request, "settings.html", {"user_form":user_form, })

@login_required
@require_POST
def vote(request):
    type_vote = request.POST['vote']
    type_object = request.POST['type_object']
    object_id = request.POST['object_id']
    user = request.user
    if type_object == 'question':
        print("tyt")
        object = Question.new_questions.get(id=object_id)
        vote = Question.hot_questions.is_liked(user, object_id)
    else:
        object = Answer.answers.get(id=object_id)
        vote = Answer.answers.is_liked(user, object_id)

    print(vote)
    if vote:
        if vote.type_vote == int(type_vote):
            vote.delete()
        elif vote.type_vote == -1:
            vote.delete()
            vote = Vote.objects.create(user=user, content_object=object, type_vote=1)
            vote.save()
        else:
            vote.delete()
            vote = Vote.objects.create(user=user, content_object=object, type_vote=-1)
            vote.save()
    else:
        print('net')
        vote = Vote.objects.create(user=user, content_object=object, type_vote=type_vote)
        vote.save()

    likes = object.votes.likes().count()
    print(likes)
    # likes=0
    # dislikes=0
    dislikes = object.votes.dislikes().count()
    print(dislikes)
    response_data = {}
    response_data['likes'] = likes
    response_data['dislikes'] = dislikes
    return HttpResponse(json.dumps(response_data),content_type="application/json")


@login_required
@require_POST
def correct_answer(request):
    print(request.GET)
    answer_id = request.POST['answer_id']
    question_id = request.POST['question_id']
    print((answer_id))
    answer = Answer.answers.get(id = answer_id)
    question = Question.new_questions.get(id=question_id)
    if question.author == request.user:
        if answer.is_correct:
            answer.is_correct = False
        else:
            answer.is_correct = True
    answer.save()
    print(answer.is_correct)
    return JsonResponse({'is_correct':answer.is_correct})


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Not found!</h1>')



