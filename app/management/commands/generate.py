
from django.core.management.base import BaseCommand
from app.models import Profile, Question, Answer, Tag, Like, LikeAnswer
from django.contrib.auth.models import User

import requests
import random
import string

class Command(BaseCommand):
    help = 'Test command'
    RANDOM_API_KEY = 'a16853c3b8e54910ab071b3b799a5233'
    RANDOM_TEXT_APY = 'https://randommer.io/api/Text/LoremIpsum'
    RANDOM_NAME_API = 'https://randommer.io/api/Name'

    SCALE = 1000
    user_numbers = 10000 //SCALE
    questions_numbers = 100000//SCALE
    answers_numbers = 1000000//SCALE
    tags_numbers = 10000//SCALE
    likes_number = 2000000//SCALE

    avatars_set = ['avatars/жираф_VRB7DGE.jpg', 'avatars/пингвин_naiSuQI.jpg', 'avatars/пес_JKIswUy.jpg',
                   'avatars/овца_pFS74YT.jpeg','avatars/кот_KMdPgLD.jpeg']

    def __init__(self):
        super().__init__()
        self.text_dataset = self.generate_words_dataset()
        self.names_set = self.generate_names_set()

    def generate_words_dataset(self):
        params = {'loremType': 'normal', 'type': 'paragraphs', 'number': 100}
        r = requests.get(
            self.RANDOM_TEXT_APY,
            params=params,
            headers={'X-Api-Key': self.RANDOM_API_KEY}
        )
        return r.text.split()

    def generate_names_set(self):
        params = {'nameType': 'surname', 'quantity': 5000}
        r = requests.get(
            self.RANDOM_NAME_API,
            params=params,
            headers={'X-Api-Key': self.RANDOM_API_KEY}
        )
        return r.json()

    def generate_random_string(self, length):
        letters = string.ascii_lowercase
        rand_string = ''.join(random.choice(letters) for i in range(length))
        return rand_string

    def create_users_and_ref_profiles(self):
        count = 0
        used_names =[]
        print(self.text_dataset)
        for i in range(self.user_numbers):
            if len(self.names_set) == 0:
                self.names_set = self.generate_names_set()
            name_choice = self.names_set.pop()

            while name_choice in used_names:
                if len(self.names_set) == 0:
                    self.names_set = self.generate_names_set()
                name_choice = self.names_set.pop()
            count +=1
            print(count)
            used_names.append(name_choice)
            user = User(username=name_choice, password=random.choice(self.text_dataset), is_staff=False, is_active=True,
                        is_superuser=False, email =  f'{random.choice(self.text_dataset)}@mail.ru')
            user.save()
            profile = Profile(user=user, avatar=random.choice(self.avatars_set))
            profile.save()

    def create_tag(self):
        uses_tag = []
        self.tags_set = []
        count = 0
        for i in range(self.tags_numbers):
            count_len = random.randrange(3,15,1)
            tag = self.generate_random_string(count_len)
            while tag in uses_tag:
                tag = self.generate_random_string(count_len)
            uses_tag.append(tag)
            count += 1
            print(count)
            self.tags_set.append(Tag(tag=tag))

        Tag.tags.bulk_create(self.tags_set)

    def generate_text(self, min, max):
        count_worlds = random.randrange(min, max, 1)
        text = ""
        for j in range(count_worlds):
            text = text + random.choice(self.text_dataset) + ' '
        return text

    def create_question_tags(self, question_id):
        count_tags = random.randrange(1, 4)
        questions_tags = []
        for tag in range(count_tags):
            tag_k_id = random.randint(1, self.tags_numbers)
            questions_tags.append(Question.tag.throught(tag_id=tag_k_id, question_id=question_id))
        Question.tag.all().bulk_create(questions_tags)



    def create_question(self):
        count = 0
        for i in range(self.questions_numbers):
            title = self.generate_text(3, 20)
            title = title + '?'
            content = self.generate_text(20, 250)
            author_id = random.randint(1, self.user_numbers)

            question = Question(title=title, content=content, author_id = author_id, rating = random.randint(0,100))
            question.save()
            count += 1
            print(count)

            count_tags = random.randrange(1, 4)
            for k in range(count_tags):
                question.tag.add(random.choice(Tag.tags.all()))


    def create_answer(self):
        answer_set =[]
        count = 0
        for i in range(self.answers_numbers):
            content = self.generate_text(30,300)
            author_id = random.randint(1, self.user_numbers)
            is_correct = random.choice(['True', 'False'])
            rating = random.randint(0,100)
            question_id = random.randint(1, self.questions_numbers)
            count += 1
            print(count)
            answer_set.append(Answer(content = content, author_id = author_id, is_correct = is_correct, rating = rating,
                            question_id = question_id))

        Answer.answers.all().bulk_create(answer_set)

    def create_likes(self):
        likes_set = []
        for i in range(self.likes_number):
            question_id = random.randint(1,self.questions_numbers)

            author_id = random.randint(1, self.user_numbers)
            likes_set.append(Like(author_id = author_id, question_id = question_id))
        Like.likes.all().bulk_create(likes_set)

    def create_likes_answer(self):
        likes_set = []
        for i in range(self.likes_number):
            answer_id = random.randint(1,self.answers_numbers)

            author_id = random.randint(1, self.user_numbers)
            likes_set.append(LikeAnswer(author_id = author_id, answer_id = answer_id))
        LikeAnswer.likes.all().bulk_create(likes_set)

    def handle(self, *args, **options):
        self.create_users_and_ref_profiles()
        self.stdout.write(self.style.SUCCESS('Users and profiles created'))
        self.create_tag()
        self.stdout.write(self.style.SUCCESS('Tags created'))
        self.create_question()
        self.stdout.write(self.style.SUCCESS('Questions created'))
        self.create_answer()
        self.stdout.write(self.style.SUCCESS('Answers created'))
        self.create_likes()
        self.stdout.write(self.style.SUCCESS('Likes created'))
        self.create_likes_answer()
        self.stdout.write(self.style.SUCCESS('Likes answer created'))


