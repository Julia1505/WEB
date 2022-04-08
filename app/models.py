from django.db import models

# Create your models here.
from django.urls import reverse

class TopUserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('rating')[:5]

class User(models.Model):
    nickname = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to="avatars/")
    register_date = models.DateField(auto_now_add=True)
    rating = models.IntegerField()

    users = models.Manager()
    top_users = TopUserManager()



    def __str__(self):
        return self.nickname

    class Meta:
        ordering = ['nickname']

class TopTagManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('count')[:7]

class Tag(models.Model):
    tag = models.CharField(max_length=30)
    count = models.IntegerField(null=True)

    tags = models.Manager()
    top_tags = TopTagManager()

    # @property
    # def num_of_questions(self):
    #     return self.questions.count()

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag', kwargs = {'slug':self.tag})

    class Meta:
        ordering = ['count', 'tag']

class HotQustionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('rating')

class Question(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateField(auto_now_add=True)
    tag = models.ManyToManyField(Tag, related_name='questions')
    rating = models.IntegerField()

    new_questions = models.Manager()
    hot_questions = HotQustionManager()

    def get_absolute_url(self):
        return reverse('question', kwargs={'id':self.pk})

    def __str__(self):
        return self.title

    # def save(self, *args, **kwargs):


    class Meta:
        ordering = ["create_date"]

class Answer(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_create = models.DateField(auto_now_add=True)
    is_correct = models.BooleanField(default=False)
    rating = models.IntegerField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, related_name='answers')

    answers = models.Manager()

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['rating', 'is_correct']

# class Rating(models.Model):
#     quesion_rat = models.OneToOneField(Question, on_delete=models.CASCADE)
#     answer_rat = models.OneToOneField(Answer, on_delete=models.CASCADE)
#     total_rat = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
