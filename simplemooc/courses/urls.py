from django.conf.urls import url
from django.urls import path

from simplemooc.courses.views import index, details, enrollment, undo_enrollment, \
    lessons, show_lesson, material, CourseView

urlpatterns = [
    path('', CourseView.as_view(), name='index'),
    path('tag/<tag>/', CourseView.as_view(), name='index_tagged'),

    # path('', index, name='index'),
    path('<slug>/', details, name='details'),
    path('<slug>/inscricao/', enrollment, name='enrollment'),

    path('<slug>/cancelar-inscricao/', undo_enrollment, name='undo_enrollment'),
    path('<slug>/aulas/', lessons, name='lessons'),
    path('<slug>/aula/<pk>/', show_lesson, name='show_lesson'),
    path('<slug>/materiais/<pk>/', material, name='material'),
]