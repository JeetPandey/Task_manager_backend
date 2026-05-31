from rest_framework import serializers
from .models import Task, Comment


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task

        fields = '__all__'
    

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source = 'user.username', read_only =True)

    class Meta:
        model = Comment
        fields = '__all__'