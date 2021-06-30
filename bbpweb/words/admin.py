from django.contrib import admin
from .models import (
    Post,
    ParallaxImages,
    Subscriber,
    Project,
)


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Post, PostAdmin)
admin.site.register(ParallaxImages)
admin.site.register(Subscriber)
admin.site.register(Project, ProjectAdmin)


admin.site.index_title = "bbp Settings"
