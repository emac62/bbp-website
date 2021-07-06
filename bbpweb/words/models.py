from django.db import models
from tinymce import models as tinymce_models
from taggit.managers import TaggableManager
from django.urls import reverse
from django.utils import timezone


class Post(models.Model):

    title = models.CharField(max_length=200)
    slug = models.SlugField()
    content = tinymce_models.HTMLField()
    post_image = models.ImageField(
        upload_to="images/", height_field=None, width_field=None, max_length=None
    )
    tags = TaggableManager()
    is_published = models.BooleanField(default=False)
    published_date = models.DateTimeField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ["-created_on"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.is_published and self.published_date is None:
            self.published_date = timezone.now()
        elif not self.is_published and self.published_date is not None:
            self.published_date = None
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})


class Project(models.Model):
    title = title = models.CharField(max_length=200)
    slug = models.SlugField()
    image1 = models.ImageField(upload_to="images/")
    alt1 = models.CharField(max_length=50)
    image2 = models.ImageField(upload_to="images/")
    alt2 = models.CharField(max_length=50)
    image3 = models.ImageField(upload_to="images/")
    alt3 = models.CharField(max_length=50)
    image4 = models.ImageField(upload_to="images/")
    alt4 = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("project-detail", kwargs={"pk": self.pk})



class ParallaxImages(models.Model):
    parallax_image = models.ImageField(
        upload_to="images/", height_field=None, width_field=None, max_length=None
    )
    parallax_image_alt = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Parallax Images"
        verbose_name_plural = "Parallax Images"

    def __str__(self):
        return self.parallax_image_alt

    def get_absolute_url(self):
        return reverse("ParallaxImages_detail", kwargs={"pk": self.pk})


class Subscriber(models.Model):
    name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=254)

    class Meta:
        verbose_name = "Subscriber"
        verbose_name_plural = "Subscribers"

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse("subscriber_detail", kwargs={"pk": self.pk})
