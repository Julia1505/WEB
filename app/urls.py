from django.urls import path
from app import views

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
]

