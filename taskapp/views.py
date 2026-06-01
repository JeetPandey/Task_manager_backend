from django.shortcuts import render
from .models import Task,Comment
from .serializers import TaskSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class TaskListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        tasks = Task.objects.all().order_by('position')
        search = request.GET.get("search")
        status_filter = request.GET.get("status")
        priority_filter = request.GET.get("priority")
        sort = request.GET.get("sort")

        if search:
            tasks = tasks.filter(
                Q(name__icontains = search)

                |

                Q(code__icontains = search)
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
        page_number = request.GET.get('page',1)
        paginator = Paginator(tasks,10)
        page_obj = paginator.get_page(page_number)
        
        serializer = TaskSerializer(page_obj,many=True)
        print(serializer)
        return Response({

        "total_pages": paginator.num_pages,

        "current_page": page_obj.number,

        "total_tasks": paginator.count,

        "results": serializer.data
        })


    
    
    def post(self,request):
        if not request.user.is_staff:
            return Response(
                {"error":"Only admin can create tasks"},
                            status=status.HTTP_403_FORBIDDEN
                            )
        serializer = TaskSerializer(data=request.data)
        
        if serializer.is_valid():
            print(serializer.initial_data)
            
            print(serializer.validated_data)
            serializer.save()
            print(serializer.data)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class TaskDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
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
        if not request.user.is_staff:
            return Response({"error":"only admin can edit task"},status=status.HTTP_403_FORBIDDEN)

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
        if not request.user.is_staff:
            return Response({"error":"only admin can delete task"},status=status.HTTP_403_FORBIDDEN)
        task = self.get_object(pk)
        if not task:
            return  Response(
                {"error":"Task not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        else:
            task.delete()
            return Response({"message":"Task deleted"}, status= status.HTTP_200_OK)
        
        


#creating the temporary view for testing the jwt authentication
class TestAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        return Response({

            "username":
            request.user.username

        })
    


class TaskStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):

        task = Task.objects.filter(pk=pk).first()

        if not task:

            return Response(
                {
                    "error":
                    "Task not found"
                },
                status=404
            )

        status_value = request.data.get('status')

        if not status_value:

            return Response(
                {
                    "error":
                    "Status required"
                },
                status=400
            )

        task.status = status_value

        task.save()

        return Response(
            {
                "message":
                "Status updated",

                "status":
                task.status
            }
        )