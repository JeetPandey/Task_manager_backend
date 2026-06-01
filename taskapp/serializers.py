from rest_framework import serializers
from .models import Task, Comment


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task

        fields = '__all__'
    

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source = 'user.username', read_only =True)
    task_name = serializers.CharField(source = 'task.name',read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'task',
            'task_name',
            'user',
            'username',
            'comment',
            'created_at'
        ]
        read_only_fields = [
            'user'
        ]