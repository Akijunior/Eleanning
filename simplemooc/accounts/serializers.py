from django.contrib.auth.models import User
from rest_framework import serializers

from simplemooc.courses.models import Course
from .models import User

from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'name']

class CourseSerializer(TaggitSerializer, serializers.ModelSerializer):

    tags = TagListSerializerField()

    class Meta:
        model = Course
        fields = '__all__'