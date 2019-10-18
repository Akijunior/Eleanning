from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, ListView

from simplemooc.courses.decorators import enrollment_required
from .forms import ContactCourse, CommentLessonForm
from .models import Course, Enrollment, Material, Lesson


class CourseView(ListView):

    paginate_by = 2
    template_name = 'courses/index.html'

    def get_queryset(self):
        queryset = Course.objects.all()

        tag = self.kwargs.get('tag', '')
        if tag:
            queryset = queryset.filter(tags__slug__icontains=tag)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(CourseView, self).get_context_data(**kwargs)
        context['tags'] = Course.tags.all()
        return context

# class CourseView(DetailView):
#
#     model = Course
#     template_name = 'forum/Course.html'
#
#     def get(self, request, *args, **kwargs):
#         response = super(CourseView, self).get(request, *args, **kwargs)
#         if not self.request.user.is_authenticated() or \
#             (self.object.author != self.request.user):
#             self.object.views = self.object.views + 1
#             self.object.save()
#         return response
#
#     def get_context_data(self, **kwargs):
#         context = super(CourseView, self).get_context_data(**kwargs)
#         context['tags'] = Course.tags.all()
#         context['form'] = ReplyForm(self.request.POST or None)
#         return context
#
#     def post(self, request, *args, **kwargs):
#         if not self.request.user.is_authenticated():
#             messages.error(self.request, 'Para responder ao tópico é necessário estar logado.')
#             return redirect(self.request.path)
#         self.object = self.get_object()
#         context = self.get_context_data(object=self.object)
#         form = context['form']
#         if form.is_valid():
#             reply = form.save(commit=False)
#             reply.Course = self.object
#             reply.author = self.request.user
#             reply.save()
#             messages.success(self.request, 'A sua resposta foi enviada com sucesso.')
#             context['form'] = ReplyForm()
#         return self.render_to_response(context)

def index(request):
    courses = Course.objects.all()  # Pegando todos os objetos cadastrados no BD
    template_name = 'courses/index.html'
    context = {
        'courses': courses
    }
    return render(request, template_name, context)


def details(request, slug):
    course = get_object_or_404(Course, slug=slug)
    isSubscribed = False

    if (Enrollment.objects.filter(Q(course=course) & Q(user=request.user)).exists()):
        isSubscribed = True

    context = {}
    form = ContactCourse(request.POST or None)

    if form.is_valid():
        context['is_valid'] = True
        print(form.cleaned_data)
        form.send_mail(course)
        form = ContactCourse()

    else:
        form = ContactCourse()

    context['form'] = form
    context['course'] = course
    context['isSubscribed'] = isSubscribed

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
        form = CommentLessonForm()
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









