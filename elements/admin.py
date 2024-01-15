from django.contrib import admin
from django.utils.text import slugify

from .models import Category, Type, Element

# Register your models here.

class ElementInline(admin.StackedInline):
    model = Element

@admin.register(Category,Type)
class CategoryTypeAdmin(admin.ModelAdmin):
    list_display = ('id','title')
    # inlines = [
    #     ElementInline
    # ]

@admin.display(description="ID and title in uppercase")
def upper_title(obj):
    return f"{obj.id} - {obj.title}".upper()
    
@admin.register(Element)
class ElementAdmin(admin.ModelAdmin):
    list_display = ('id','title','category','type', upper_title, 'cheap')
    # fields = (('title','slug'),'description','price',('category','type'))
    # fields = ('title','slug','description','price','category','type')
    fieldsets = [
        (
            "Regular options",
            {
                "fields":(('title','slug'),'description',('category','type'))
            }
        ),
        (
            "Advanced options",
            {
                "fields":('price',),
                "classes": ['collapse']
            }
        )
    ]

    def save_model(self, request, obj, form, change):

        if not(change) and obj.slug == '':
            obj.slug = slugify(obj.title)

        if obj.slug == '':
            obj.slug = slugify(obj.title)

        super().save_model(request, obj, form, change)
