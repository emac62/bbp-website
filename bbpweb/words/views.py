from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, TemplateView
from .models import MainPageImages, PhotosPageImages, Post, ParallaxImages, Project
from taggit.models import Tag
from django.template import context
from .forms import ContactForm, SubscribeForm
from django.core.mail import EmailMessage
from django.db.models import Q
from django.contrib import messages
from .models import Subscriber


class TagMixin(object):
    def get_context_data(self, **kwargs):
        context = super(TagMixin, self).get_context_data(**kwargs)
        context["tags"] = Tag.objects.all()
        return context


class HomeView(ListView):
    model = Project
    template_name = "words/home.html"
    title = "Home"
    context_object_name = "projects"
    qs = Project.objects.defer(
        "image2",
        "alt2",
        "image3",
        "alt3",
        "image4",
        "alt4",
    )

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context["latest"] = Post.objects.filter(is_published=True).first()
        context["parallax_img"] = ParallaxImages.objects.first()
        return context


class WordsView(TagMixin, ListView):
    model = Post
    template_name = "words/words.html"
    context_object_name = "posts"
    qs = Post.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super(WordsView, self).get_context_data(**kwargs)
        context["latest"] = Post.objects.filter(is_published=True).first()
        context["title"] = "Words"
        context["form"] = SubscribeForm()
        return context


class PhotosView(ListView):
    model = Project
    template_name = "words/photos.html"
    title = "Photos"
    context_object_name = "projects"
    qs = Project.objects.all()

    def get_context_data(self, **kwargs):
        context = super(PhotosView, self).get_context_data(**kwargs)
        context["parallax_img"] = ParallaxImages.objects.last()
        context["form"] = ContactForm()
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = "words/project.html"
    title = "Photo Project"

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        return context

    def get(self, request, pk):
        project = Project.objects.get(pk=pk)
        context = locals()
        return render(request, self.template_name, context)


class WordsDetailView(DetailView):
    model = Post
    template_name = "words/words.html"
    title = "Words"

    def get_context_data(self, **kwargs):
        context = super(WordsDetailView, self).get_context_data(**kwargs)
        return context

    def get(self, request, pk):
        latest = Post.objects.get(pk=pk)
        posts = Post.objects.all()
        tags = Tag.objects.all()
        form = SubscribeForm()
        context = locals()
        return render(request, self.template_name, context)


class TagListView(TagMixin, ListView):
    model = Post
    template_name = "words/words.html"
    title = "Search"

    def get_context_data(self, **kwargs):
        context = super(TagListView, self).get_context_data(**kwargs)
        context["results"] = Post.objects.filter(tags__slug=self.kwargs.get("slug"))
        context["posts"] = Post.objects.all()
        context["form"] = SubscribeForm()
        context["title"] = "Search"
        return context


class SearchListView(TagMixin, ListView):
    model = Post
    template_name = "words/words.html"
    title = "Search"

    def get(self, request, *args, **kwargs):
        query = request.GET.get("q", "")
        self.results = Post.objects.filter(content__icontains=query)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SearchListView, self).get_context_data(
            results=self.results, **kwargs
        )
        context["posts"] = Post.objects.all()
        context["form"] = SubscribeForm()
        context["title"] = "Search"
        return context


class PrivacyPolicy(TemplateView):
    template_name = "words/privacy.html"
    title = "Privacy Policy"


def contact(request):
    form = ContactForm()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            cf = form.cleaned_data
            # now in the object cf, you have the form as a dictionary.
            name = cf.get("name")
            subject = cf.get("subject")
            email = cf.get("email")
            message = cf.get("message")

        email_message = EmailMessage(
            subject=name + " : " + subject,
            body=message,
            to=["bobbiebphotography@gmail.com"],
            headers={"Reply-To": email},
        )

        email_message.send()
        return redirect("photos")


def subscribe(request):
    form = SubscribeForm()
    if request.method == "POST":
        form = SubscribeForm(request.POST)
        if form.is_valid():
            cf = form.cleaned_data
            # now in the object cf, you have the form as a dictionary.
            name = cf.get("name")
            email = cf.get("email")

            if Subscriber.objects.filter(email=email).exists():
                messages.success(request, "We already have that email on file.")
                return redirect("words")
            form.save()
            messages.success(request, "Thank you.")

        return redirect("words")
