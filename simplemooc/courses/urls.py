from django.conf.urls import url
from django.urls import path

from simplemooc.courses.views import index, details, enrollment, undo_enrollment, announcements, show_announcement, \
    lessons, show_lesson, material

urlpatterns = [
    path('', index, name='index'),
    #path('?P<pk>\d+)/$', details, name='details'),
    path('<slug>/', details, name='details'),
    path('<slug>//inscricao/', enrollment, name='enrollment'),

    path('<slug>/cancelar-inscricao/', undo_enrollment, name='undo_enrollment'),
    path('<slug>/anuncios/', announcements, name='announcements'),
    path('<slug>/anuncios/<pk>/', show_announcement, name='show_announcement'),
    path('<slug>/aulas/', lessons, name='lessons'),
    path('<slug>/aula/<pk>/', show_lesson, name='show_lesson'),
    path('<slug>/materiais/<pk>/', material, name='material'),
]