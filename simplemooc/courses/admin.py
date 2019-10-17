from django.contrib import admin
from django.apps import apps
from .models import Course, Enrollment, Material, Lesson

# Registrar os modelos aqui.

#Definindo opções para customização do model no admin do Django
# class CourseAdmin(admin.ModelAdmin):
#     list_display = ['nome', 'slug', 'start_date','create_at']
#     search_fields = ['nome','slug']
#     prepopulated_fields = {'slug': ('nome',)} #Populando o slug de acordo com o nome do curso de forma automatica
#
# admin.site.register(Course, CourseAdmin)
# admin.site.register(Enrollment)


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


