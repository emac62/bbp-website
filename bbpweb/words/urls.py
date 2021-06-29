from django.urls import path

from . import views
from .views import (
    HomeView,
    PhotosView,
    WordsView,
    WordsDetailView,
    TagListView,
    ProjectDetailView,
    SearchListView,
    PrivacyPolicy,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("words/", WordsView.as_view(), name="words"),
    path("photos/", PhotosView.as_view(), name="photos"),
    path("words/<int:pk>/", WordsDetailView.as_view(), name="details"),
    path("words/tag/<str:slug>", TagListView.as_view(), name="tagged"),
    path("words/search_results", SearchListView.as_view(), name="search"),
    path("words/contact", views.contact, name="contact"),
    path("words/subscribe", views.subscribe, name="subscribe"),
    path("words/project/<int:pk>", ProjectDetailView.as_view(), name="project-detail"),
    path("privacy/", PrivacyPolicy.as_view(), name="privacy"),
]
