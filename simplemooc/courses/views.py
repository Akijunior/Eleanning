from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from simplemooc.courses.decorators import enrollment_required
from .forms import ContactCourse, CommentForm, CommentLessonForm
from .models import Course, Enrollment, Material, Lesson, Announcement


# Create your views here.

# Resposavel por randerizar o template para a listagem de cursos
def index(request):
    courses = Course.objects.all()  # Pegando todos os objetos cadastrados no BD
    template_name = 'courses/index.html'
    context = {
        'courses': courses
    }
    return render(request, template_name, context)


def details(request, slug):
    course = get_object_or_404(Course, slug=slug)
    context = {}
    if request.method == 'POST':
        form = ContactCourse(request.POST)
        if form.is_valid():
            context['is_valid'] = True
            print(form.cleaned_data)
            form.send_mail(course)
            form = ContactCourse()

    else:
        form = ContactCourse()
    context['form'] = form
    context['course'] = course
    template_name = 'courses/details.html'
    return render(request, template_name, context)


@login_required
def enrollment(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user, course=course
    )

    if created:
        messages.success(request, 'Inscrição efetuada com sucesso')
    else:
        messages.info(request, 'Você já está inscrito no curso')

    return redirect('accounts:dashboard')


@login_required
def undo_enrollment(resquest, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment = get_object_or_404(
        Enrollment, user=resquest.user, course=course
    )
    if resquest.method == 'POST':
        enrollment.delete()
        messages.success(resquest, 'Sua inscrição foi cancelada com sucesso.')
        return redirect('accounts:dashboard')
    template_name = 'courses/undo_enrollment.html'
    context = {
        'enrollment': enrollment,
        'course': course,
    }
    return render(resquest, template_name, context)


@login_required
@enrollment_required
def announcements(resquest, slug):
    course = resquest.course
    template_name = 'courses/announcements.html'
    context = {
        'course': course,
        'announcements': course.announcements.all()
    }
    return render(resquest, template_name, context)


@login_required
@enrollment_required
def show_announcement(resquest, slug, pk):
    course = get_object_or_404(Course, slug=slug)
    announcement = get_object_or_404(Announcement, pk=pk)
    form = CommentForm(resquest.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = resquest.user
        comment.announcement = announcement
        comment.save()
        form = CommentForm()
        messages.success(resquest, 'Seu comentário foi enviado com sucesso.')
    template_name = 'courses/show_announcement.html'
    context = {
        'course': course,
        'announcement': announcement,
        'form': form,
    }
    return render(resquest, template_name, context)


@login_required
@enrollment_required
def lessons(resquest, slug):
    course = resquest.course
    template_name = 'courses/lessons.html'
    lessons = course.release_lessons()
    if resquest.user.is_staff:
        lessons = course.lessons.all()
    context = {
        'course': course,
        'lessons': lessons
    }
    return render(resquest, template_name, context)


@login_required
@enrollment_required
def show_lesson(resquest, slug, pk):
    course = get_object_or_404(Course, slug=slug)
    lesson = get_object_or_404(Lesson, pk=pk, course=course)

    form = CommentLessonForm(resquest.POST or None)

    if not resquest.user.is_staff and not lesson.is_available():
        messages.error(resquest, 'Esta aula não está disponível')
        return redirect('courses:lessons', slug=course.slug)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = resquest.user
        comment.lesson = lesson
        comment.save()
        form = CommentForm()
        messages.success(resquest, 'Seu comentário foi enviado com sucesso.')
    template_name = 'courses/show_lesson.html'

    context = {
        'course': course,
        'lesson': lesson,
        'form': form,
    }
    return render(resquest, template_name, context)


@login_required
@enrollment_required
def material(resquest, slug, pk):
    course = resquest.course
    material = get_object_or_404(Material, pk=pk, lesson__course=course)
    lesson = material.lesson
    if not resquest.user.is_staff and not lesson.is_available():
        messages.error(resquest, 'Esse material não está disponível')
        return redirect('courses:lesson', slug=course.slug, pk=lesson.pk)
    if not material.is_embedded():
        return redirect(material.archive.url)
    template_name = 'courses/material.html'
    context = {
        'course': course,
        'material': material,
        'lesson': lesson
    }
    return render(resquest, template_name, context)









