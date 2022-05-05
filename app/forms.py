from django import forms
from django.core.exceptions import ValidationError

from .models import *

# class SearchForm(forms.Form):
#     query = forms.CharField()


class LoginForm(forms.Form):
    username = forms.CharField(label="Your login", max_length=20, widget=forms.TextInput(attrs={'placeholder':'Your login', 'autocomplete':"off", 'class':"form-control log_in ",}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':"form-control log_in", 'placeholder':'Your password'}), max_length=20, )

    def clean_password(self):
        data = self.cleaned_data['password']
        if len(data) < 4:
            raise ValidationError("Password should be more than 3 symbols")
        return data

# class SignUpForm(forms.ModelForm):
#     class Meta:
#         model = User
#
#

# class RegisterForm(forms.ModelForm):
#     password_one = forms.CharField()
#     password_two = forms.CharField()
#     avatar = forms.ImageField()
#
#     class Meta:
#         model = User
#         fields = ['username', 'email']
#
#     def save(self, commit=True):

class ProfileFrom(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']

    def clean(self):
        password_one = self.cleaned_data['password_one']
        password_two = self.cleaned_data['password_two']
        if password_one != password_two:
            raise forms.ValidationError("Пароли не совпадают")
        else:
            return self.cleaned_data['password_one']

#
class QuestionForm(forms.ModelForm):

    def __init__(self, user, **kwargs):
        self._user = user
        super(QuestionForm, self).__init__(**kwargs)


    def save(self, commit=True):
        self.cleaned_data['author'] = self._user
        instance = Question.new_questions.create(title=self.cleaned_data['title'],
        content=self.cleaned_data['content'], author=self.cleaned_data['author'])
        for tag in self.cleaned_data['tag']:
            instance.tag.add(tag)
        print(self.cleaned_data)
        return instance


    class Meta:
        model = Question
        fields = ['title', 'content', 'tag']

        widgets = {
            'title':forms.TextInput(attrs={"class":"form-control line_new_q", 'placeholder':'Question', 'maxlength':200}),
            'content': forms.Textarea(attrs={'cols':40, 'rows':5, 'class':"form-control line_new_q",}),
            'tag':forms.SelectMultiple(attrs={"class":"form-control line_new_q"})
        }

class AnswerForm(forms.ModelForm):
    def __init__(self, user, question, **kwargs):
        self._user = user
        self._question = question
        super(AnswerForm, self).__init__(**kwargs)

    def save(self, commit=True):
        self.cleaned_data['author'] = self._user
        self.cleaned_data['question_id'] = self._question
        return Answer.answers.create(**self.cleaned_data)

    class Meta:
        model = Answer
        fields=['content']
        widgets = {
            'content':forms.Textarea(attrs={"class":"form-control", "cols":40, "rows":7})
        }


