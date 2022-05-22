from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from django.urls import reverse

class TopProfileManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('-rating')[:5]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to="avatars/", default='def.jpeg', blank=True, null=True)
    rating = models.IntegerField(null=True)

    users = models.Manager()
    top_users = TopProfileManager()

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['-rating']

class VoteManager(models.Manager):
    use_for_related_fields = True

    def likes(self):
        return self.get_queryset().filter(type_vote__gt=0).all()

    def dislikes(self):
        return self.get_queryset().filter(type_vote__lt=0).all()

    def sum_rating(self):
        return self.get_queryset().aggregate(Sum('type_vote')).get('type_vote__sum') or 0  #???



class Vote(models.Model):
    LIKE = 1
    DISLIKE = -1
    VOTES = (
        (DISLIKE, "Dislike"),
        (LIKE, "Like"),
    )

    type_vote = models.SmallIntegerField(choices=VOTES)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    # question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='votes')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, default=None)
    object_id = models.PositiveIntegerField(default=None)
    content_object = GenericForeignKey()

    objects = VoteManager()

    # def __str__(self):
    #     return self.type_vote


class TopTagManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(num_quest = Count('questions')).order_by('-num_quest')[:7]


class Tag(models.Model):
    tag = models.CharField(max_length=30, unique=True)

    tags = models.Manager()
    top_tags = TopTagManager()


    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag', kwargs={'slug': self.tag})

    class Meta:
        ordering = ['tag']


class HotQustionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(num_likes=Count('votes')).order_by('-num_likes')

    def is_liked(self, user_id, object_id):
        vote = self.get(id=object_id).votes.all().filter(user_id=user_id).first()
        return vote


class Question(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateField(auto_now_add=True)
    tag = models.ManyToManyField(Tag, related_name='questions')
    votes = GenericRelation(Vote, related_query_name='questions')
    # rating = models.IntegerField()

    new_questions = models.Manager()
    hot_questions = HotQustionManager()

    def get_absolute_url(self):
        return reverse('question', kwargs={'id': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["create_date"]

class AnswerManager(models.Manager):
    def is_liked(self, user_id, object_id):
        vote = self.get(id=object_id).votes.all().filter(user_id=user_id).first()
        return vote

class Answer(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_create = models.DateField(auto_now_add=True)
    is_correct = models.BooleanField(default=False)
    # rating = models.IntegerField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, related_name='answers')
    votes = GenericRelation(Vote, related_query_name='answers')


    answers = AnswerManager()

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['-is_correct']


