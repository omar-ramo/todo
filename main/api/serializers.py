from rest_framework import serializers

from ..models import Task


class TaskBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'slug', 'created_on',
                  'do_before', 'done', 'finished_on']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'slug', 'created_on',
        		  'updated_on', 'do_before', 'done', 'finished_on']
