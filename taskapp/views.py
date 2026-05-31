from django.shortcuts import render
from .models import Task,Comment
from .serializers import TaskSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q

# Create your views here.


class TaskListCreateAPIView(APIView):
    def get(self,request):
        tasks = Task.objects.order_by('position')
        search = request.Get.get("search")
        status_filter = request.Get.get("status")
        priority_filter = request.Get.get("priority")
        sort = request.Get.get("sort")

        if search:
            tasks = tasks.filter(
                Q(name__icontains = search)

                |

                Q(name__icontains = search)
            )
        
        if status_filter:
            tasks = tasks.filter(
                status = status_filter
            )
        if priority_filter:
            tasks = tasks.filter(
                priority=priority_filter
            )
        if sort == 'due_date':
            tasks = tasks.order_by(
                'due_date'
            )
        serializer = TaskSerializer(tasks,many=True)
        print(serializer)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = TaskSerializer(data=request.data)
        
        if serializer.is_valid():
            print(serializer.initial_data)
            print(serializer.data)
            print(serializer.validated_data)
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class TaskDetailAPIView(APIView):
    def get_object(self,pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return None
        
    def get(self,request,pk):
        task = self.get_object(pk)
        if not task:
            return  Response(
                {"error":"Task not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        serilizer = TaskSerializer(task)
        return Response(serilizer.data)
    
    def put(self,request,pk):
        task = self.get_object(pk)

        if not task:
            return  Response(
                {"error":"Task not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        else:
            serializer = TaskSerializer(task,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
    
    def delete(self,request,pk):
        task = self.get_object(pk)
        if not task:
            return  Response(
                {"error":"Task not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        else:
            task.delete()
            return Response({"message":"Task deleted"}, status= status.HTTP_200_OK)
        
        


