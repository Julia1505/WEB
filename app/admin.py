from django.contrib import admin

# Register your models here.
from app.models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'nickname', 'register_date', 'rating')
    list_display_links = ('id', 'nickname')
    search_fields = ('id', 'nickname')

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'create_date', 'rating')
    list_display_links = ('id', 'title')
    search_fields = ('id', 'title', 'tag')

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'author', 'is_correct', 'rating')
    list_display_links = ('id', 'question')
    search_fields = ('id', 'question', 'author')
    list_editable = ('is_correct',)

class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag', 'count')
    list_filter = ('tag', 'count')
    search_fields = ('id', 'tag')
    # prepopulated_fields = {'slug':('tag',)}

admin.site.register(User, UserAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Tag, TagAdmin)


