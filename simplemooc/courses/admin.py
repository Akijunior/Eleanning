from django.contrib import admin
from django.apps import apps
from .models import Material, Lesson

register_all_models_from = [
    'courses', 'accounts'
]

class MaterialInlineAdmin(admin.StackedInline):

    model = Material

class LessonAdmin(admin.ModelAdmin):

    list_display = ['name', 'number', 'course', 'release_date']
    search_fields = ['name', 'description']
    list_filter = ['created_at']

    inlines = [
        MaterialInlineAdmin
    ]

for app in register_all_models_from:
    for name, obj in apps.all_models[app].items():
        if (name != 'lesson'):
            admin.site.register(obj)

admin.site.register(Lesson, LessonAdmin)


