from django.contrib import admin

from .models import Comment
# Register your models here.

# @admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # list_display = ('id', 'text')
    # search_fields = ('id', 'text')
    # date_hierarchy = 'date_posted'
    # ordering = ('date_posted',)
    # list_filter = ('id', 'date_posted')
    # list_editable = ('text',)
    fields = ('text',)
    # exclude = ('element',)
    save_as=True
    save_on_top=True

    class Media:
        css = {
            "all" : ['my_style.css']
        }




    # def delete_queryset(self, request, queryset):
    #     print('delete')
    #     super().delete_queryset(request, queryset)

    # def save_model(self, request, obj, form, change):
    #     super().save_model(request, obj, form, change)
    #     print('after')

admin.site.register(Comment, CommentAdmin)

