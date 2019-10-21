from rest_framework import routers

from simplemooc.accounts.viewsets import UserViewSet, CourseViewSet

router = routers.DefaultRouter()
router.register(r'usuarios', UserViewSet, base_name='usuario')
router.register(r'cursos', CourseViewSet, base_name='curso')
