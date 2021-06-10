from django.contrib import admin
from .models import (
    Post,
    MainPageImages,
    PhotosPageImages,
    ParallaxImages,
    Subscriber,
    Project,
)


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Post, PostAdmin)
admin.site.register(MainPageImages)
admin.site.register(PhotosPageImages)
admin.site.register(ParallaxImages)
admin.site.register(Subscriber)
admin.site.register(Project, ProjectAdmin)
