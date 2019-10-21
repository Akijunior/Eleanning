from django.conf import settings
from django.db import models
# Create your models here.
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager

from simplemooc.core.mail import send_mail_template


class CourseManager(models.Manager):

    def search(self, query):
        return self.get_queryset().filter(
            models.Q(nome__icontains=query) | \
            models.Q(description__icontains=query)
        )


class Course(models.Model):

    nome = models.CharField('Nome', max_length=100)
    slug = models.SlugField('Atalho')
    description = models.TextField('Descrição Simples', blank=True)
    about = models.TextField('Sobre o Curso', blank=True)
    start_date = models.DateField(
        'Data de Início', null=True, blank=True
    )
    image = models.ImageField(
        upload_to='courses/images', verbose_name='Imagem',
        null=True, blank=True
    )

    create_at = models.DateTimeField('Criado em', auto_now_add=True)
    update_at = models.DateTimeField('Atualizado em', auto_now=True)
    objects = CourseManager()

    tags = TaggableManager()

    # Metodo para retornar o nome do curso.
    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('courses:details', args=[self.slug])

    def release_lessons(self):
        today = timezone.now().date()
        # release_date__gte -> filtro se é maior ou igual
        return self.lessons.filter(release_date__gte=today)

    # Customizando o admin
    class Meta:
        verbose_name = 'Curso'  # Vai associar ao nome da classe
        verbose_name_plural = 'Cursos'
        ordering = ['nome']  # Ordenando resultados pelo nome


class Lesson(models.Model):
    name = models.CharField('Nome', max_length=100)
    description = models.TextField('Descrição', blank=True)
    number = models.IntegerField('Número (ordem)', blank=True, default=0)
    release_date = models.DateField('Data de Liberação', blank=True, null=True)

    course = models.ForeignKey(Course, verbose_name='Curso', related_name='lessons', on_delete=models.CASCADE)

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return self.name

    def is_available(self):
        if self.release_date:
            today = timezone.now().date()
            return self.release_date >= today
        return False

    class Meta:
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'
        ordering = ['number']


class LessonComment(models.Model):


    lesson = models.ForeignKey(
        Lesson, verbose_name='Aula', related_name='comments', on_delete=models.CASCADE
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuário', on_delete=models.CASCADE)
    comment = models.TextField('Comentário')

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Comentário da Aula'
        verbose_name_plural = 'Comentários das Aulas'
        ordering = ['created_at']

class Material(models.Model):
    name = models.CharField('Nome', max_length=100)
    embedded = models.TextField('Video embedded', blank=True)
    archive = models.FileField(upload_to='lessons/materials', blank=True, null=True)

    lesson = models.ForeignKey(Lesson, verbose_name='Aula', related_name='materials', on_delete=models.CASCADE)

    def is_embedded(self):
        return bool(self.embedded)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materiais'


class Enrollment(models.Model):
    ''' Inscrição em um curso '''

    STATUS_CHOICES = (
        (0, 'Pendente'),
        (1, 'Aprovado'),
        (2, 'Cancelado'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Usuário',
        related_name='enrollments', on_delete=models.CASCADE
    )
    course = models.ForeignKey(
        Course, verbose_name='Curso', related_name='enrollments', on_delete=models.CASCADE
    )
    status = models.IntegerField(
        'Situação', choices=STATUS_CHOICES, default=1,
        blank=True
    )

    create_at = models.DateTimeField('Criado em', auto_now_add=True)
    update_at = models.DateTimeField('Atualizado em', auto_now=True)

    def active(self):
        self.status = 1
        self.save()

    def is_approved(self):
        return self.status == 1

    class Meta:
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'
        unique_together = (('user', 'course'))
        # Indicando que para esse model, deve criar um indice de unicidade para cada usuário e curso

    def __str__(self):
        return "Inscrição"



def post_save_announcement(instance, created, **kwargs):
    if created:
        subject = instance.title
        template_name = 'courses/announcement_mail.html'
        context = {
            'announcement': instance
        }
        enrollments = Enrollment.objects.filter(course=instance.course, status=1)
        for enrollment in enrollments:
            recipient_list = [enrollment.user.email]
            send_mail_template(subject, template_name, context, recipient_list)

