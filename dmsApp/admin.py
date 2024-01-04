from django.contrib import admin
from .models import Post

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'description', 'file_path', 'date_created', 'date_updated')
    list_filter = ('user', 'title', 'date_created', 'date_updated')
    search_fields = ('user', 'title', 'description', 'file_path', 'date_created', 'date_updated')
    readonly_fields = ('date_created', 'date_updated')
    # prepopulated_fields = {'slug': ('title',)}
    # ordering = ('user', 'title', 'date_created', 'date_updated')
    # filter_horizontal = ()
    # fieldsets = ()
