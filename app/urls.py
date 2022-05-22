from django.conf.urls.static import static
from django.urls import path
from app import views
from ask_me import settings

urlpatterns = [
    path('', views.index, name="home"),
    path('hot/', views.hot, name="hot"),
    path('question/<int:id>/', views.question, name="question"),
    path('ask/', views.ask, name="ask"),
    path('login/', views.login, name="login"),
    path('settings/', views.settings, name="settings"),
    path('tag/<str:slug>/', views.tag, name="tag"),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.logout, name='logout'),
    path('vote/',views.vote, name='vote-view'),
    path('vote_answer/',views.vote, name='vote-answer-view'),
    path('correct_answer/', views.correct_answer, name='correct_answer')
] + static(settings.STATIC_URL, document_root = settings.STATICFILES_DIRS) \
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

